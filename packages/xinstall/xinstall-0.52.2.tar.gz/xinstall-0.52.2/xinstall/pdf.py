"""PDF related tools.
"""
from .utils import (
    is_debian_series,
    is_fedora_series,
    update_apt_source,
    brew_install_safe,
    is_macos,
    run_cmd,
    add_subparser,
    option_pip_bundle,
)


def pdftotext(args):
    """Install the Python library pdftotext.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            run_cmd(
                f"""{args.prefix} apt-get {args.yes_s} install build-essential libpoppler-cpp-dev pkg-config \
                    && {args.pip_install} pdftotext
                """
            )
        if is_macos():
            brew_install_safe(["pkg-config", "poppler"])
            run_cmd("{args.pip_install} pdftotext")
        if is_fedora_series():
            run_cmd(
                f"""{args.prefix} yum install {args.yes_s} gcc-c++ pkgconfig poppler-cpp-devel \
                    && {args.pip_install} pdftotext
                    """
            )
    if args.uninstall:
        run_cmd(f"{args.pip_uninstall} pdftotext")


def _add_subparser_pdftotext(subparsers):
    add_subparser(
        subparsers,
        "pdftotext",
        func=pdftotext,
        aliases=["ptt", "p2t"],
        add_argument=_pdftotext_args
    )


def _pdftotext_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_pdf(subparsers):
    _add_subparser_pdftotext(subparsers)
