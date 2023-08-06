# Copyright (c) 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import os

import click

from platformio.commands.boards import print_boards
from platformio.exception import UserSideException
from platformio.package.exception import UnknownPackageError
from platformio.package.manager.platform import PlatformPackageManager
from platformio.package.meta import PackageItem, PackageSpec
from platformio.package.version import get_original_version
from platformio.platform.exception import UnknownPlatform
from platformio.platform.factory import PlatformFactory


@click.group(short_help="Platform manager", hidden=True)
def cli():
    pass


@cli.command("search", short_help="Search for development platform")
@click.argument("query", required=False)
@click.option("--json-output", is_flag=True)
def platform_search(query, json_output):
    if not json_output:
        click.secho(
            "\nWARNING: This command is deprecated and will be removed in "
            "the next releases. \nPlease use `pio pkg search` instead.\n",
            fg="yellow",
        )
    platforms = []
    for platform in _get_registry_platforms():
        if query == "all":
            query = ""
        search_data = json.dumps(platform)
        if query and query.lower() not in search_data.lower():
            continue
        platforms.append(
            _get_registry_platform_data(
                platform["name"], with_boards=False, expose_packages=False
            )
        )

    if json_output:
        click.echo(json.dumps(platforms))
    else:
        _print_platforms(platforms)


@cli.command("frameworks", short_help="List supported frameworks, SDKs")
@click.argument("query", required=False)
@click.option("--json-output", is_flag=True)
def platform_frameworks(query, json_output):
    regclient = PlatformPackageManager().get_registry_client_instance()
    frameworks = []
    for framework in regclient.fetch_json_data(
        "get", "/v2/frameworks", x_cache_valid="1d"
    ):
        if query == "all":
            query = ""
        search_data = json.dumps(framework)
        if query and query.lower() not in search_data.lower():
            continue
        framework["homepage"] = "https://platformio.org/frameworks/" + framework["name"]
        framework["platforms"] = [
            platform["name"]
            for platform in _get_registry_platforms()
            if framework["name"] in platform["frameworks"]
        ]
        frameworks.append(framework)

    frameworks = sorted(frameworks, key=lambda manifest: manifest["name"])
    if json_output:
        click.echo(json.dumps(frameworks))
    else:
        _print_platforms(frameworks)


@cli.command("list", short_help="List installed development platforms")
@click.option("--json-output", is_flag=True)
def platform_list(json_output):
    if not json_output:
        click.secho(
            "\nWARNING: This command is deprecated and will be removed in "
            "the next releases. \nPlease use `pio pkg list` instead.\n",
            fg="yellow",
        )
    platforms = []
    pm = PlatformPackageManager()
    for pkg in pm.get_installed():
        platforms.append(
            _get_installed_platform_data(pkg, with_boards=False, expose_packages=False)
        )

    platforms = sorted(platforms, key=lambda manifest: manifest["name"])
    if json_output:
        click.echo(json.dumps(platforms))
    else:
        _print_platforms(platforms)


@cli.command("show", short_help="Show details about development platform")
@click.argument("platform")
@click.option("--json-output", is_flag=True)
def platform_show(platform, json_output):  # pylint: disable=too-many-branches
    if not json_output:
        click.secho(
            "\nWARNING: This command is deprecated and will be removed in "
            "the next releases. \nPlease use `pio pkg show` instead.\n",
            fg="yellow",
        )
    data = _get_platform_data(platform)
    if not data:
        raise UnknownPlatform(platform)
    if json_output:
        return click.echo(json.dumps(data))

    dep = "{ownername}/{name}".format(**data) if "ownername" in data else data["name"]
    click.echo(
        "{dep} ~ {title}".format(dep=click.style(dep, fg="cyan"), title=data["title"])
    )
    click.echo("=" * (3 + len(dep + data["title"])))
    click.echo(data["description"])
    click.echo()
    if "version" in data:
        click.echo("Version: %s" % data["version"])
    if data["homepage"]:
        click.echo("Home: %s" % data["homepage"])
    if data["repository"]:
        click.echo("Repository: %s" % data["repository"])
    if data["url"]:
        click.echo("Vendor: %s" % data["url"])
    if data["license"]:
        click.echo("License: %s" % data["license"])
    if data["frameworks"]:
        click.echo("Frameworks: %s" % ", ".join(data["frameworks"]))

    if not data["packages"]:
        return None

    if not isinstance(data["packages"][0], dict):
        click.echo("Packages: %s" % ", ".join(data["packages"]))
    else:
        click.echo()
        click.secho("Packages", bold=True)
        click.echo("--------")
        for item in data["packages"]:
            click.echo()
            click.echo("Package %s" % click.style(item["name"], fg="yellow"))
            click.echo("-" * (8 + len(item["name"])))
            if item["type"]:
                click.echo("Type: %s" % item["type"])
            click.echo("Requirements: %s" % item["requirements"])
            click.echo(
                "Installed: %s" % ("Yes" if item.get("version") else "No (optional)")
            )
            if "version" in item:
                click.echo("Version: %s" % item["version"])
            if "originalVersion" in item:
                click.echo("Original version: %s" % item["originalVersion"])
            if "description" in item:
                click.echo("Description: %s" % item["description"])

    if data["boards"]:
        click.echo()
        click.secho("Boards", bold=True)
        click.echo("------")
        print_boards(data["boards"])

    return True


@cli.command("install", short_help="Install new development platform")
@click.argument("platforms", nargs=-1, required=True, metavar="[PLATFORM...]")
@click.option("--with-package", multiple=True)
@click.option("--without-package", multiple=True)
@click.option("--skip-default-package", is_flag=True)
@click.option("--with-all-packages", is_flag=True)
@click.option("-s", "--silent", is_flag=True, help="Suppress progress reporting")
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Reinstall/redownload dev/platform and its packages if exist",
)
def platform_install(  # pylint: disable=too-many-arguments,too-many-locals
    platforms,
    with_package,
    without_package,
    skip_default_package,
    with_all_packages,
    silent,
    force,
):
    click.secho(
        "\nWARNING: This command is deprecated and will be removed in "
        "the next releases. \nPlease use `pio pkg install` instead.\n",
        fg="yellow",
    )

    def _find_pkg_names(p, candidates):
        result = []
        for candidate in candidates:
            found = False
            # lookup by package types
            for _name, _opts in p.packages.items():
                if _opts.get("type") == candidate:
                    result.append(_name)
                    found = True
            if (
                p.frameworks
                and candidate.startswith("framework-")
                and candidate[10:] in p.frameworks
            ):
                result.append(p.frameworks[candidate[10:]]["package"])
                found = True
            if not found:
                result.append(candidate)
        return result

    pm = PlatformPackageManager()
    pm.set_log_level(logging.WARN if silent else logging.DEBUG)
    for platform in platforms:
        if with_package or without_package or with_all_packages:
            pkg = pm.install(platform, skip_dependencies=True)
            p = PlatformFactory.new(pkg)
            if with_all_packages:
                with_package = list(p.packages)
            with_package = set(_find_pkg_names(p, with_package or []))
            without_package = set(_find_pkg_names(p, without_package or []))
            upkgs = with_package | without_package
            ppkgs = set(p.packages)
            if not upkgs.issubset(ppkgs):
                raise UnknownPackageError(", ".join(upkgs - ppkgs))
            for name, options in p.packages.items():
                if name in without_package:
                    continue
                if name in with_package or not (
                    skip_default_package or options.get("optional", False)
                ):
                    p.pm.install(p.get_package_spec(name), force=force)
        else:
            pkg = pm.install(platform, skip_dependencies=skip_default_package)

        if pkg and not silent:
            click.secho(
                "The platform '%s' has been successfully installed!\n"
                "The rest of the packages will be installed later "
                "depending on your build environment." % platform,
                fg="green",
            )


@cli.command("uninstall", short_help="Uninstall development platform")
@click.argument("platforms", nargs=-1, required=True, metavar="[PLATFORM...]")
def platform_uninstall(platforms):
    click.secho(
        "\nWARNING: This command is deprecated and will be removed in "
        "the next releases. \nPlease use `pio pkg uninstall` instead.\n",
        fg="yellow",
    )
    pm = PlatformPackageManager()
    pm.set_log_level(logging.DEBUG)
    for platform in platforms:
        if pm.uninstall(platform):
            click.secho(
                "The platform '%s' has been successfully removed!" % platform,
                fg="green",
            )


@cli.command("update", short_help="Update installed development platforms")
@click.argument("platforms", nargs=-1, required=False, metavar="[PLATFORM...]")
@click.option(
    "-p", "--only-packages", is_flag=True, help="Update only the platform packages"
)
@click.option(
    "-c",
    "--only-check",
    is_flag=True,
    help="DEPRECATED. Please use `--dry-run` instead",
)
@click.option(
    "--dry-run", is_flag=True, help="Do not update, only check for the new versions"
)
@click.option("-s", "--silent", is_flag=True, help="Suppress progress reporting")
@click.option("--json-output", is_flag=True)
def platform_update(  # pylint: disable=too-many-locals, too-many-arguments
    platforms, only_check, dry_run, silent, json_output, **_
):
    if only_check and not json_output:
        raise UserSideException(
            "This command is deprecated, please use `pio pkg outdated` instead"
        )

    if not json_output:
        click.secho(
            "\nWARNING: This command is deprecated and will be removed in "
            "the next releases. \nPlease use `pio pkg update` instead.\n",
            fg="yellow",
        )

    pm = PlatformPackageManager()
    pm.set_log_level(logging.WARN if silent else logging.DEBUG)
    platforms = platforms or pm.get_installed()
    only_check = dry_run or only_check

    if only_check and json_output:
        result = []
        for platform in platforms:
            spec = None
            pkg = None
            if isinstance(platform, PackageItem):
                pkg = platform
            else:
                spec = PackageSpec(platform)
                pkg = pm.get_package(spec)
            if not pkg:
                continue
            outdated = pm.outdated(pkg, spec)
            if (
                not outdated.is_outdated(allow_incompatible=True)
                and not PlatformFactory.new(pkg).are_outdated_packages()
            ):
                continue
            data = _get_installed_platform_data(
                pkg, with_boards=False, expose_packages=False
            )
            if outdated.is_outdated(allow_incompatible=True):
                data["versionLatest"] = (
                    str(outdated.latest) if outdated.latest else None
                )
            result.append(data)
        return click.echo(json.dumps(result))

    for platform in platforms:
        click.echo(
            "Platform %s"
            % click.style(
                platform.metadata.name
                if isinstance(platform, PackageItem)
                else platform,
                fg="cyan",
            )
        )
        click.echo("--------")
        pm.update(platform)
        click.echo()

    return True


#
# Helpers
#


def _print_platforms(platforms):
    for platform in platforms:
        click.echo(
            "{name} ~ {title}".format(
                name=click.style(platform["name"], fg="cyan"), title=platform["title"]
            )
        )
        click.echo("=" * (3 + len(platform["name"] + platform["title"])))
        click.echo(platform["description"])
        click.echo()
        if "homepage" in platform:
            click.echo("Home: %s" % platform["homepage"])
        if "frameworks" in platform and platform["frameworks"]:
            click.echo("Frameworks: %s" % ", ".join(platform["frameworks"]))
        if "packages" in platform:
            click.echo("Packages: %s" % ", ".join(platform["packages"]))
        if "version" in platform:
            if "__src_url" in platform:
                click.echo(
                    "Version: %s (%s)" % (platform["version"], platform["__src_url"])
                )
            else:
                click.echo("Version: " + platform["version"])
        click.echo()


def _get_registry_platforms():
    regclient = PlatformPackageManager().get_registry_client_instance()
    return regclient.fetch_json_data("get", "/v2/platforms", x_cache_valid="1d")


def _get_platform_data(*args, **kwargs):
    try:
        return _get_installed_platform_data(*args, **kwargs)
    except UnknownPlatform:
        return _get_registry_platform_data(*args, **kwargs)


def _get_installed_platform_data(platform, with_boards=True, expose_packages=True):
    p = PlatformFactory.new(platform)
    data = dict(
        name=p.name,
        title=p.title,
        description=p.description,
        version=p.version,
        homepage=p.homepage,
        url=p.homepage,
        repository=p.repository_url,
        license=p.license,
        forDesktop=not p.is_embedded(),
        frameworks=sorted(list(p.frameworks) if p.frameworks else []),
        packages=list(p.packages) if p.packages else [],
    )

    # if dump to API
    # del data['version']
    # return data

    # overwrite VCS version and add extra fields
    manifest = PlatformPackageManager().legacy_load_manifest(
        os.path.dirname(p.manifest_path)
    )
    assert manifest
    for key in manifest:
        if key == "version" or key.startswith("__"):
            data[key] = manifest[key]

    if with_boards:
        data["boards"] = [c.get_brief_data() for c in p.get_boards().values()]

    if not data["packages"] or not expose_packages:
        return data

    data["packages"] = []
    installed_pkgs = {
        pkg.metadata.name: p.pm.load_manifest(pkg) for pkg in p.get_installed_packages()
    }
    for name, options in p.packages.items():
        item = dict(
            name=name,
            type=p.get_package_type(name),
            requirements=options.get("version"),
            optional=options.get("optional") is True,
        )
        if name in installed_pkgs:
            for key, value in installed_pkgs[name].items():
                if key not in ("url", "version", "description"):
                    continue
                item[key] = value
                if key == "version":
                    item["originalVersion"] = get_original_version(value)
        data["packages"].append(item)

    return data


def _get_registry_platform_data(  # pylint: disable=unused-argument
    platform, with_boards=True, expose_packages=True
):
    _data = None
    for p in _get_registry_platforms():
        if p["name"] == platform:
            _data = p
            break

    if not _data:
        return None

    data = dict(
        ownername=_data.get("ownername"),
        name=_data["name"],
        title=_data["title"],
        description=_data["description"],
        homepage=_data["homepage"],
        repository=_data["repository"],
        url=_data["url"],
        license=_data["license"],
        forDesktop=_data["forDesktop"],
        frameworks=_data["frameworks"],
        packages=_data["packages"],
        versions=_data.get("versions"),
    )

    if with_boards:
        data["boards"] = [
            board
            for board in PlatformPackageManager().get_registered_boards()
            if board["platform"] == _data["name"]
        ]

    return data
