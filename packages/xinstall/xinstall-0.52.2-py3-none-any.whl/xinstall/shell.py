"""Install shell (command-line) related tools.
"""
from pathlib import Path
import logging
import shutil
import sys
import os
import textwrap
from . import github
from .utils import (
    HOME,
    BASE_DIR,
    BIN_DIR,
    is_win,
    is_macos,
    is_linux,
    is_debian_series,
    is_fedora_series,
    update_apt_source,
    brew_install_safe,
    run_cmd,
    add_subparser,
    option_pip_bundle,
    add_path_shell,
)


def _add_subparser_shell(subparsers):
    _add_subparser_coreutils(subparsers)
    _add_subparser_change_shell(subparsers)
    _add_subparser_shell_utils(subparsers)
    _add_subparser_bash_it(subparsers)
    _add_subparser_xonsh(subparsers)
    _add_subparser_homebrew(subparsers)
    _add_subparser_hyper(subparsers)
    _add_subparser_openinterminal(subparsers)
    _add_subparser_bash_complete(subparsers)
    _add_subparser_wajig(subparsers)
    _add_subparser_exa(subparsers)
    _add_subparser_osquery(subparsers)
    _add_subparser_dust(subparsers)
    _add_subparser_rip(subparsers)
    _add_subparser_long_path(subparsers)
    _add_subparser_gh(subparsers)


def coreutils(args) -> None:
    """Install CoreUtils.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} coreutils")
        elif is_macos():
            brew_install_safe("coreutils")
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum install coreutils")
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} coreutils")
        elif is_macos():
            run_cmd("brew uninstall coreutils")
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum remove coreutils")
    if args.config:
        if is_macos():
            cmd = """export PATH=/usr/local/opt/findutils/libexec/gnubin:"$PATH" \
                && export MANPATH=/usr/local/opt/findutils/libexec/gnuman:"$MANPATH"
                """
            run_cmd(cmd)
            logging.info("GNU paths are exported.")


def _add_subparser_coreutils(subparsers) -> None:
    add_subparser(subparsers, "CoreUtils", func=coreutils, aliases=["cu"])


def shell_utils(args) -> None:
    """Install Shell-related utils.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            run_cmd(
                f"""{args.prefix} apt-get install {args.yes_s} \
                    bash-completion command-not-found man-db""",
            )
        elif is_macos():
            brew_install_safe(["bash-completion@2", "man-db"])
        elif is_fedora_series():
            run_cmd(
                f"{args.prefix} yum install bash-completion command-not-found man-db"
            )
    if args.uninstall:
        if is_debian_series():
            run_cmd(
                f"""{args.prefix} apt-get purge {args.yes_s} \
                    bash-completion command-not-found man-db""",
            )
        elif is_macos():
            run_cmd("brew uninstall bash-completion man-db")
        elif is_fedora_series():
            run_cmd(
                f"{args.prefix} yum remove bash-completion command-not-found man-db"
            )
    if args.config:
        pass


def _add_subparser_shell_utils(subparsers) -> None:
    add_subparser(
        subparsers,
        "Shell utils",
        func=shell_utils,
        aliases=["sh_utils", "shutils", "shu", "su"]
    )


def change_shell(args) -> None:
    """Change the default shell.
    """
    if is_linux():
        pass
    elif is_macos():
        run_cmd(f"{args.prefix} chsh -s {args.shell}")


def _change_shell_args(subparser) -> None:
    subparser.add_argument(
        "-s",
        "--shell",
        dest="shell",
        default="/bin/bash",
        help="the shell to change to."
    )


def _add_subparser_change_shell(subparsers) -> None:
    add_subparser(
        subparsers,
        "change shell",
        func=change_shell,
        aliases=["chsh", "cs"],
        add_argument=_change_shell_args
    )


def homebrew(args) -> None:
    """Install Homebrew.
    """
    if args.install:
        if is_macos():
            cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"'
            run_cmd(cmd)
        elif is_linux():
            cmd = "mkdir ~/homebrew && curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C ~/homebrew"
            run_cmd(cmd)
        else:
            pass
    if args.config:
        if is_linux():
            dirs = [f"{HOME}/homebrew", "/home/homebrew/.homebrew"]
            paths = [f"{dir_}/bin/brew" for dir_ in dirs if os.path.isdir(dir_)]
            if paths:
                brew = paths[-1]
                profiles = [f"{HOME}/.bash_profile", f"{HOME}/.profile"]
                for profile in profiles:
                    run_cmd(f"{brew} shellenv >> {profile}")
                logging.info(
                    "Shell environment variables for Linuxbrew are inserted to %s.",
                    profiles
                )
            else:
                sys.exit("Homebrew is not installed!")
    if args.uninstall:
        pass


def _add_subparser_homebrew(subparsers) -> None:
    add_subparser(
        subparsers,
        "Homebrew",
        func=homebrew,
        aliases=["brew"],
    )


def hyper(args) -> None:
    """Install the hyper.js terminal.
    """
    if args.install:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get update")
            args.output = "/tmp/hyper.deb"
            args.install_cmd = f"{args.prefix} apt-get install {args.yes_s}"
            github.install(args)
        elif is_macos():
            run_cmd("brew cask install hyper")
        elif is_fedora_series():
            #!yum install hyper
            pass
    if args.config:
        run_cmd("hyper i hypercwd")
        run_cmd("hyper i hyper-search")
        run_cmd("hyper i hyper-pane")
        run_cmd("hyper i hyperpower")
        logging.info(
            "Hyper plugins hypercwd, hyper-search, hyper-pane and hyperpower are installed."
        )
        path = f"{HOME}/.hyper.js"
        #if os.path.exists(path):
        #    os.remove(path)
        shutil.copy2(os.path.join(BASE_DIR, "hyper/hyper.js"), path)
        logging.info("%s is copied to %s.", BASE_DIR / "hyper/hyper.js", path)
    if args.uninstall:
        if is_debian_series():
            #!apt-get purge hyper
            pass
        elif is_macos():
            run_cmd("brew cask uninstall hyper")
        elif is_fedora_series():
            #!yum remove hyper
            pass


def _add_subparser_hyper(subparsers) -> None:
    add_subparser(subparsers, "Hyper", func=hyper, aliases=["hp"])


def openinterminal(args) -> None:
    """Install openinterminal.
    """
    if args.install:
        if is_macos():
            run_cmd("brew cask install openinterminal")
    if args.config:
        pass
    if args.uninstall:
        if is_macos():
            run_cmd("brew cask uninstall openinterminal")


def _add_subparser_openinterminal(subparsers) -> None:
    add_subparser(subparsers, "OpenInTerminal", func=openinterminal, aliases=["oit"])


def xonsh(args) -> None:
    """Install xonsh, a Python based shell.
    """
    if args.install:
        run_cmd(f"{args.pip_install} xonsh")
    if args.config:
        src = f"{BASE_DIR}/xonsh/xonshrc"
        dst = HOME / ".xonshrc"
        try:
            dst.unlink()
        except FileNotFoundError:
            pass
        shutil.copy2(src, dst)
        logging.info("%s is copied to %s.", src, dst)
    if args.uninstall:
        run_cmd(f"{args.pip_uninstall} xonsh")


def _xonsh_args(subparser) -> None:
    option_pip_bundle(subparser)


def _add_subparser_xonsh(subparsers) -> None:
    add_subparser(subparsers, "xonsh", func=xonsh, add_argument=_xonsh_args)


def bash_it(args) -> None:
    """Install Bash-it, a community Bash framework.
    For more details, please refer to https://github.com/Bash-it/bash-it#installation.
    """
    if args.install:
        dir_ = Path.home() / ".bash_it"
        try:
            dir_.unlink()
        except FileNotFoundError:
            pass
        cmd = f"""git clone --depth=1 https://github.com/Bash-it/bash-it.git {dir_} \
                && {dir_}/install.sh --silent -f
                """
        run_cmd(cmd)
    if args.config:
        profile = HOME / (".bashrc" if is_linux() else ".bash_profile")
        add_path_shell([BIN_DIR, Path.home() / ".cargo/bin"], profile)
        logging.info("'export PATH=%s:$PATH' is inserted into %s.", BIN_DIR, profile)
        if is_linux():
            bash = textwrap.dedent(
                """\
                # source in ~/.bashrc
                if [[ -f $HOME/.bashrc ]]; then
                    . $HOME/.bashrc
                fi
                """
            )
            with (HOME / ".bash_profile").open("w") as fout:
                fout.write(bash)
    if args.uninstall:
        run_cmd("~/.bash_it/uninstall.sh")
        shutil.rmtree(HOME / ".bash_it")


def _add_subparser_bash_it(subparsers) -> None:
    add_subparser(
        subparsers, "Bash-it", func=bash_it, aliases=["bashit", "shit", "bit"]
    )


def bash_completion(args) -> None:
    """Install and configure bash-complete.

    :param args:
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} bash-completion")
        elif is_macos():
            brew_install_safe(["bash-completion@2"])
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum install bash-completion")
    if args.config:
        pass
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge bash-completion")
        elif is_macos():
            run_cmd("brew uninstall bash-completion")
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum remove bash-completion")


def _add_subparser_bash_complete(subparsers) -> None:
    add_subparser(
        subparsers,
        "Bash completion",
        func=bash_completion,
        aliases=["completion", "comp", "cp"]
    )


def exa(args) -> None:
    """Install exa which is an Rust-implemented alternative to ls.
    """
    if args.install:
        if is_debian_series():
            run_cmd("cargo install --root /usr/local/ exa")
        elif is_macos():
            brew_install_safe(["exa"])
        elif is_fedora_series():
            run_cmd("cargo install --root /usr/local/ exa")
    if args.config:
        pass
    if args.uninstall:
        if is_debian_series():
            run_cmd("cargo uninstall --root /usr/local/ exa")
        elif is_macos():
            run_cmd("brew uninstall exa")
        elif is_fedora_series():
            run_cmd("cargo uninstall --root /usr/local/ exa")


def _add_subparser_exa(subparsers) -> None:
    add_subparser(subparsers, "exa", func=exa)


def osquery(args) -> None:
    """Install osquery for Linux admin.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            cmd = f"""xinstall github -r osquery/osquery -k linux amd64 deb -o /tmp/osquery.deb \
                    && {args.prefix} apt-get install {args.yes_s} /tmp/osquery.deb
                """
            run_cmd(cmd)
        elif is_macos():
            cmd = "brew install --cask osquery"
            run_cmd(cmd)
        elif is_fedora_series():
            cmd = f"""xinstall github -r osquery/osquery -k linux amd64 rpm -o /tmp/osquery.rpm \
                    && {args.prefix} yum install {args.yes_s} /tmp/osquery.rpm
                """
            run_cmd(cmd)
        elif is_win():
            cmd = """xinstall github -r osquery/osquery -k msi -o "%temp%\\osquery.msi" \
                    && msiexec /i "%temp%\\osquery.msi"
                """
            run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} osquery")
        elif is_macos():
            run_cmd("brew uninstall osquery")
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum remove osquery")
        elif is_win():
            pass


def _add_subparser_osquery(subparsers) -> None:
    add_subparser(subparsers, "osquery", func=osquery, aliases=["osq"])


def wajig(args) -> None:
    """Install wajig.
    """
    if not is_debian_series():
        return
    if args.install:
        update_apt_source(prefix=args.prefix)
        run_cmd(f"{args.prefix} apt-get install {args.yes_s} wajig")
    if args.config:
        pass
    if args.proxy:
        cmd = f"""echo '\nAcquire::http::Proxy "{args.proxy}";\nAcquire::https::Proxy "{args.proxy}";' \
            | {args.prefix} tee -a /etc/apt/apt.conf"""
        run_cmd(cmd)
    if args.uninstall:
        run_cmd(f"{args.prefix} apt-get purge {args.yes_s} wajig")


def _wajig_args(subparser) -> None:
    subparser.add_argument(
        "-p",
        "--proxy",
        dest="proxy",
        default="",
        help="Configure apt to use the specified proxy."
    )


def _add_subparser_wajig(subparsers) -> None:
    add_subparser(
        subparsers, "Wajig", func=wajig, aliases=["wj"], add_argument=_wajig_args
    )


def dust(args) -> None:
    """Install dust which is du implemented in Rust.
    The cargo command must be available on the search path in order to install dust.
    """
    if args.install:
        if is_macos():
            run_cmd("brew install dust")
        else:
            run_cmd("cargo install du-dust")
    if args.config:
        pass
    if args.uninstall:
        if is_macos():
            run_cmd("brew uninstall dust")
        else:
            run_cmd("cargo uninstall du-dust")


def _add_subparser_dust(subparsers) -> None:
    add_subparser(subparsers, "dust", func=dust, aliases=[])


def rip(args) -> None:
    """Install rip which is rm improved.
    The cargo command must be available on the search path in order to install rip.
    """
    if args.install:
        if is_macos():
            run_cmd("brew install rm-improved")
        else:
            run_cmd("cargo install rm-improved")
    if args.config:
        if is_linux():
            run_cmd(f"{args.prefix} ln -svf ~/.cargo/bin/rip /usr/local/bin")
    if args.uninstall:
        if is_macos():
            run_cmd("brew uninstall rm-improved")
        else:
            run_cmd("cargo uninstall rm-improved")


def _add_subparser_rip(subparsers) -> None:
    add_subparser(subparsers, "rip", func=rip, aliases=["trash"])


def long_path(args) -> None:
    """Enable/disable long path support on Windows.
    This command needs to be run in an admin CMD/PowerShell.
    """
    if args.config:
        if args.value is None:
            return
        value = 1 if args.value else 0
        cmd = f"""C:\\Windows\\System32\\powershell.exe New-ItemProperty `
                -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\FileSystem" `
                -Name "LongPathsEnabled" `
                -Value {value} `
                -PropertyType DWORD `
                -Force
            """
        run_cmd(cmd)


def _long_path_args(subparser) -> None:
    subparser.add_argument(
        "--enable",
        "--yes",
        "-e",
        "-y",
        dest="value",
        default=None,
        action="store_const",
        const="1",
        help="Enable long path support on Windows."
    )
    subparser.add_argument(
        "--disable",
        "--no",
        "-d",
        "-n",
        dest="value",
        action="store_const",
        const="0",
        help="Disable long path support on Windows."
    )


def _add_subparser_long_path(subparsers) -> None:
    add_subparser(
        subparsers,
        "long_path",
        func=long_path,
        aliases=["longp", "lpath", "lp"],
        add_argument=_long_path_args
    )


def gh(args) -> None:
    """Install and configure gh (GitHub cli).
    """
    if args.install:
        if is_macos():
            run_cmd("brew install gh")
        elif is_linux():
            if is_debian_series():
                cmd = f"""curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | {args.prefix} dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
                    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | {args.prefix} tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
                    && {args.prefix} apt-get update && {args.prefix} apt-get install -y gh
                    """
                run_cmd(cmd)
            elif is_fedora_series():
                cmd = f"{args.prefix} dnf install gh"
                run_cmd(cmd)
            else:
                pass
        elif is_win():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_macos():
            run_cmd("brew uninstall gh")
        elif is_linux():
            if is_debian_series():
                cmd = f"{args.prefix} apt-get purge -y gh"
                run_cmd(cmd)
            elif is_fedora_series():
                cmd = f"{args.prefix} dnf remove gh"
                run_cmd(cmd)
            else:
                pass
        elif is_win():
            pass


def _add_subparser_gh(subparsers) -> None:
    add_subparser(subparsers, "gh", func=gh, aliases=["github_cli"])
