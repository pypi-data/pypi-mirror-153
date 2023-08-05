"""GitHub related utils.
"""
from pathlib import Path
import logging
import urllib.request
import shutil
import re
import requests
from packaging.version import parse
from packaging.specifiers import SpecifierSet
from .utils import (
    option_version,
    option_pip_bundle,
    add_subparser,
    run_cmd,
)


def _add_subparser_github(subparsers):
    _add_subparser_dsutil(subparsers)
    _add_subparser_install(subparsers)


def get_latest_version(url: str) -> str:
    """Get the latest release version of a project on GitHub.

    :param url: The URL of a project on GitHub.
    :return: The latest release version of the project.
    """
    url = f"{url}/releases/latest"
    with urllib.request.urlopen(url) as resp:
        return Path(resp.url).name


def install_python_lib(
    url: str,
    user: bool = False,
    pip_option: str = "",
    extras: str = "",
    prefix: str = "",
    python: str = "python3",
) -> None:
    """Automatically install the latest version of a Python package from its GitHub repository.
    :param url: The root URL of the GitHub repository.
    :param user: If True, install to user's local directory.
        This option is equivalant to 'pip install --user'.
    :param pip_option: Extra pip options.
    :param extras: Extra components (separate by comma) of the package to install.
    :param prefix: Prefix (e.g., sudo, environment variable configuration, etc.) to the command.
    :param python: The path (default python3) to the Python executable.
    """
    ver = get_latest_version(url)
    ver_no_letter = re.sub("[a-zA-Z]", "", ver)
    name = Path(url).name
    url = f"{url}/releases/download/{ver}/{name}-{ver_no_letter}-py3-none-any.whl"
    if extras:
        url = f"'{name}[{extras}] @ {url}'"
    cmd = f"{prefix} {python} -m pip install {'--user' if user else ''} --upgrade {pip_option} {url}"
    run_cmd(cmd)


def get_release_url(repo: str) -> str:
    """Get the release URL of a project on GitHub.

    :param repo: The repo name of the project on GitHub.
    :return: The release URL of the project on GitHub.
    """
    if repo.endswith(".git"):
        repo = repo[:-4]
    if repo.startswith("https://api."):
        return repo
    if repo.startswith("https://"):
        rindex = repo.rindex("/")
        index = repo.rindex("/", 0, rindex)
        repo = repo[(index + 1):]
    elif repo.startswith("git@"):
        index = repo.rindex(":")
        repo = repo[(index + 1):]
    return f"https://api.github.com/repos/{repo}/releases"


def download(args):
    """Download a release from GitHub.

    :param args: The arguments to parse. 
        If None, the arguments from command-line are parsed.
    """
    if args.version:
        v0 = args.version[0]
        if v0.isdigit():
            args.version = "==" + args.version
        elif v0 == "v":
            args.version = "==" + args.version[1:]
    spec = SpecifierSet(args.version)
    # get asserts of the first release in the specifier
    resp = requests.get(get_release_url(args.repo))
    if not resp.ok:
        resp.raise_for_status()
    releases = resp.json()
    assets = next(
        release["assets"] for release in releases if parse(release["tag_name"]) in spec
    )
    # get download URL
    if args.keyword:
        filter_ = lambda name: all(kwd in name for kwd in args.keyword)
    else:
        filter_ = lambda name: True
    url = next(
        asset["browser_download_url"] for asset in assets if filter_(asset["name"])
    )
    # download the assert
    logging.info("Downloading assert from the URL: %s", url)
    resp = requests.get(url, stream=True)
    if not resp.ok:
        resp.raise_for_status()
    with open(args.output, "wb") as fout:
        shutil.copyfileobj(resp.raw, fout)


def install(args) -> None:
    """Download packages from GitHub and then install and configure it.

    :param args: The arguments to parse. 
        If None, the arguments from command-line are parsed.
    """
    download(args)
    if args.install_cmd:
        run_cmd(f"{args.install_cmd} {args.output}")


def _install_args(subparser):
    subparser.add_argument(
        "-r",
        "--repo",
        "--repository",
        dest="repo",
        required=True,
        help="The GitHub repository from which to download the package.",
    )
    option_version(
        subparser,
        help="The version specifier of the package to download/install/configure."
    )
    subparser.add_argument(
        "-k",
        "--kwd",
        "--keyword",
        dest="keyword",
        nargs="+",
        default=(),
        help="The keywords that assert's name must contain.",
    )
    subparser.add_argument(
        "-o",
        "--output",
        dest="output",
        required=True,
        help="The output path for the downloaded assert.",
    )
    subparser.add_argument(
        "--cmd",
        "--install-cmd",
        dest="install_cmd",
        default="",
        help="The output path for the downloaded assert.",
    )


def _add_subparser_install(subparsers) -> None:
    add_subparser(
        subparsers,
        "install_from_github",
        func=install,
        aliases=["from_github"],
        add_argument=_install_args,
    )


def dsutil(args) -> None:
    """Install the Python package dsutil.
    """
    if args.install:
        url = "https://github.com/dclong/dsutil"
        install_python_lib(
            url=url,
            user=args.user,
            pip_option=args.pip_option,
            extras=args.extras,
            prefix=args.prefix,
            python=args.python,
        )
    if args.config:
        pass
    if args.uninstall:
        run_cmd(f"{args.prefix} {args.pip_uninstall} dsutil")


def _dsutil_args(subparser) -> None:
    option_pip_bundle(subparser)
    subparser.add_argument(
        "-e",
        "--extras",
        dest="extras",
        default="",
        help="Extra components to install."
    )


def _add_subparser_dsutil(subparsers) -> None:
    add_subparser(
        subparsers, "dsutil", func=dsutil, aliases=[], add_argument=_dsutil_args
    )
