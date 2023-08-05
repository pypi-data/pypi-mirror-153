"""The command-line interface for xinstall.
"""
import logging
from argparse import ArgumentParser, Namespace
from .utils import USER, is_win
from .ai import _add_subparser_ai
from .shell import _add_subparser_shell
from .ide import _add_subparser_ide
from .github import _add_subparser_github
from .dev import _add_subparser_dev
from .bigdata import _add_subparser_bigdata
from .jupyter import _add_subparser_jupyter
from .virtualization import _add_subparser_virtualization
from .network import _add_subparser_network
from .desktop import _add_subparser_desktop
from .pdf import _add_subparser_pdf

__version__ = "0.52.2"


def version(args):  # pylint: disable=W0613
    """Print the version of xinstall.
    """
    print(__version__)


def _add_subparser_version(subparsers):
    subparser = subparsers.add_parser(
        "version", aliases=["ver", "v"], help="Print version of the xinstall package."
    )
    subparser.set_defaults(func=version)
    return subparser


def parse_args(args=None, namespace=None) -> Namespace:
    """Parse command-line arguments.
    
    :param args: The arguments to parse. 
        If None, the arguments from command-line are parsed.
    :param namespace: An inital Namespace object.
    :return: A namespace object containing parsed options.
    """
    parser = ArgumentParser(
        description="Easy installation and configuration for Unix/Linux"
    )
    parser.add_argument(
        "-l", "--level", dest="level", default="INFO", help="The level of logging."
    )
    parser.add_argument(
        "-y",
        "--yes",
        dest="yes",
        action="store_true",
        help="Automatical yes (default no) to prompt questions."
    )
    parser.add_argument(
        "--prefix",
        dest="prefix",
        default="",
        help="The prefix command (e.g., sudo) to use."
    )
    parser.add_argument(
        "--sudo",
        dest="prefix",
        action="store_const",
        const="sudo",
        help="The prefix command (e.g., sudo) to use."
    )
    subparsers = parser.add_subparsers(dest="sub_cmd", help="Sub commands.")
    _add_subparser_version(subparsers)
    _add_subparser_ide(subparsers)
    _add_subparser_dev(subparsers)
    _add_subparser_bigdata(subparsers)
    _add_subparser_github(subparsers)
    _add_subparser_ai(subparsers)
    _add_subparser_network(subparsers)
    _add_subparser_pdf(subparsers)
    _add_subparser_jupyter(subparsers)
    _add_subparser_desktop(subparsers)
    _add_subparser_shell(subparsers)
    _add_subparser_virtualization(subparsers)
    # --------------------------------------------------------
    args = parser.parse_args(args=args, namespace=namespace)
    args.yes_s = "--yes" if args.yes else ""
    if "user" in args:
        args.user_s = "--user" if args.user else ""
    if USER == "root" or is_win():
        args.prefix = ""
    if "pip_option" in args:
        if args.pip_option:
            args.pip_option = " ".join(
                f"--{option}" for option in args.pip_option.split(",")
            )
        args.pip_install = f"{args.python} -m pip install {args.user_s} {args.pip_option}"
        args.pip_uninstall = f"{args.python} -m pip uninstall"
        args.jupyterlab = f"{args.python} -m jupyterlab"
        args.jupyter = f"{args.python} -m jupyter"
        args.ipython = f"{args.python} -m IPython"
    return args


def main():
    """Run xinstall command-line interface.
    """
    args = parse_args()
    logging.basicConfig(
        format=
        "%(asctime)s | %(module)s.%(funcName)s: %(lineno)s | %(levelname)s: %(message)s",
        level=getattr(logging, args.level.upper())
    )
    logging.debug("Command-line options:\n%s", args)
    args.func(args)


if __name__ == "__main__":
    main()
