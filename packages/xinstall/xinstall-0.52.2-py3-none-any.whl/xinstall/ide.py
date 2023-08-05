"""Install IDE related tools.
"""
from typing import Union
from pathlib import Path
from argparse import Namespace
#import logging
import os
import shutil
import re
from .utils import (
    USER, HOME, BASE_DIR, BIN_DIR, LOCAL_DIR, is_debian_series, is_fedora_series,
    update_apt_source, brew_install_safe, is_macos, run_cmd, add_subparser,
    intellij_idea_plugin, option_pip_bundle
)


def vim(args) -> None:
    """Install Vim.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} vim vim-nox")
        elif is_macos():
            brew_install_safe(["vim"])
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum install {args.yes_s} vim-enhanced")
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} vim vim-nox")
        elif is_macos():
            run_cmd("brew uninstall vim")
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum remove vim")
    if args.config:
        pass


def _add_subparser_vim(subparsers) -> None:
    add_subparser(subparsers, "Vim", func=vim)


def neovim(args) -> None:
    """Install NeoVim.
    """
    if args.ppa and is_debian_series():
        args.install = True
        run_cmd(f"{args.prefix} add-apt-repository -y ppa:neovim-ppa/unstable")
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} neovim")
        elif is_macos():
            brew_install_safe(["neovim"])
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum install neovim")
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} neovim")
        elif is_macos():
            run_cmd("brew uninstall neovim")
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum remove neovim")
    if args.config:
        pass


def _neovim_args(subparser) -> None:
    subparser.add_argument(
        "--ppa",
        dest="ppa",
        action="store_true",
        help="Install the unstable version of NeoVim from PPA."
    )


def _add_subparser_neovim(subparsers) -> None:
    add_subparser(
        subparsers, "NeoVim", func=neovim, aliases=["nvim"], add_argument=_neovim_args
    )


def _svim_true_color(true_color: Union[bool, None]) -> None:
    """Enable/disable true color for SpaceVim.
    """
    if true_color is None:
        return
    file = HOME / ".SpaceVim.d/init.toml"
    with file.open() as fin:
        lines = fin.readlines()
    for idx, line in enumerate(lines):
        if line.strip().startswith("enable_guicolors"):
            if true_color:
                lines[idx] = line.replace("false", "true")
            else:
                lines[idx] = line.replace("true", "false")
    with file.open("w") as fout:
        fout.writelines(lines)


def _strip_spacevim(args: Namespace) -> None:
    if not args.strip:
        return
    dir_ = Path.home() / ".SpaceVim/"
    paths = [
        ".git",
        ".SpaceVim.d/",
        ".ci/",
        ".github/",
        "docker/",
        "docs/",
        "wiki/",
        ".editorconfig",
        ".gitignore",
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.cn.md",
        "CONTRIBUTING.md",
        "Makefile",
        "README.cn.md",
        "README.md",
        "codecov.yml",
    ]
    for path in paths:
        path = dir_ / path
        if path.is_file():
            try:
                path.unlink()
            except FileNotFoundError:
                pass
        else:
            try:
                shutil.rmtree(path)
            except FileNotFoundError:
                pass


def spacevim(args) -> None:
    """Install and configure SpaceVim.
    """
    if args.install:
        run_cmd("curl -sLf https://spacevim.org/install.sh | bash")
        _strip_spacevim(args)
        if shutil.which("nvim"):
            run_cmd('nvim --headless +"call dein#install()" +qall')
        if not args.no_lsp:
            cmd = f"{args.pip_install} python-language-server[all] pyls-mypy"
            # npm install -g bash-language-server javascript-typescript-langserver
            run_cmd(cmd)
    if args.config:
        # configure .SpaceVim
        des_dir = HOME / ".SpaceVim"
        os.makedirs(des_dir, exist_ok=True)
        shutil.copy2(BASE_DIR / "SpaceVim/SpaceVim/init.vim", des_dir)
        # configure .SpaceVim.d
        des_dir = HOME / ".SpaceVim.d"
        os.makedirs(des_dir, exist_ok=True)
        shutil.copy2(BASE_DIR / "SpaceVim/SpaceVim.d/init.toml", des_dir)
        shutil.copy2(BASE_DIR / "SpaceVim/SpaceVim.d/vimrc", des_dir)
        # -----------------------------------------------------------
        _svim_true_color(args.true_colors)
        #_svim_for_firenvim()
    if args.uninstall:
        run_cmd("curl -sLf https://spacevim.org/install.sh | bash -s -- --uninstall")


def _svim_for_firenvim():
    file = HOME / ".SpaceVim/init.vim"
    with file.open("a") as fout:
        fout.write('\n"' + "-" * 79 + "\n")
        fout.write("if exists('g:started_by_firenvim')\n")
        fout.write("    set guifont=Monaco:h16\n")
        fout.write("endif\n")


def _spacevim_args(subparser) -> None:
    subparser.add_argument(
        "--enable-true-colors",
        dest="true_colors",
        action="store_true",
        default=None,
        help="Enable true color (default true) for SpaceVim."
    )
    subparser.add_argument(
        "--disable-true-colors",
        dest="true_colors",
        action="store_false",
        help="Disable true color (default true) for SpaceVim."
    )
    subparser.add_argument(
        "--no-lsp",
        dest="no_lsp",
        action="store_true",
        help="Disable true color (default true) for SpaceVim."
    )
    subparser.add_argument(
        "--strip",
        dest="strip",
        action="store_true",
        help='Strip unnecessary files from "~/.SpaceVim".'
    )
    option_pip_bundle(subparser)


def _add_subparser_spacevim(subparsers) -> None:
    add_subparser(
        subparsers,
        "SpaceVim",
        func=spacevim,
        aliases=["svim"],
        add_argument=_spacevim_args
    )


def bash_lsp(args) -> None:
    """Install Bash Language Server for SpaceVim.
    """
    if args.install:
        cmd = f"{args.prefix} npm install -g bash-language-server"
        run_cmd(cmd)
    if args.config:
        toml = HOME / ".SpaceVim.d/init.toml"
        with toml.open("r") as fin:
            lines = [
                '  "sh",' if re.search(r"^\s*#\s*(\"|')sh(\"|'),\s*$", line) else line
                for line in fin
            ]
        with toml.open("w") as fout:
            fout.writelines(lines)
    if args.uninstall:
        cmd = f"{args.prefix} npm uninstall bash-language-server"
        run_cmd(cmd)


def _add_subparser_bash_lsp(subparsers) -> None:
    add_subparser(subparsers, "Bash LSP", func=bash_lsp, aliases=["blsp"])


def ideavim(args) -> None:
    """Install IdeaVim for IntelliJ.
    """
    if args.config:
        shutil.copy2(BASE_DIR / "ideavim/ideavimrc", HOME / ".ideavimrc")


def _add_subparser_ideavim(subparsers) -> None:
    add_subparser(subparsers, "IdeaVim", func=ideavim, aliases=["ivim"])


def intellij_idea(args) -> None:
    """Install IntelliJ IDEA.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            des_dir = f"{LOCAL_DIR}/share/ide/idea"
            executable = f"{BIN_DIR}/idea"
            if USER == "root":
                des_dir = "/opt/idea"
                executable = "/opt/idea/bin/idea.sh"
            cmd = f"""{args.prefix} apt-get install -y ubuntu-make \
                && umake ide idea {des_dir} \
                && ln -s {des_dir}/bin/idea.sh {executable}"""
            run_cmd(cmd)
        elif is_macos():
            run_cmd("brew cask install intellij-idea-ce")
        elif is_fedora_series():
            pass
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} intellij-idea-ce")
        elif is_macos():
            run_cmd("brew cask uninstall intellij-idea-ce")
        elif is_fedora_series():
            pass
    if args.config:
        pass


def visual_studio_code(args) -> None:
    """Install Visual Studio Code.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} vscode")
        elif is_macos():
            run_cmd("brew cask install visual-studio-code")
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum install vscode")
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} vscode")
        elif is_macos():
            run_cmd("brew cask uninstall visual-studio-code")
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum remove vscode")
    if args.config:
        src_file = f"{BASE_DIR}/vscode/settings.json"
        if not args.user_dir:
            args.user_dir = f"{HOME}/.config/Code/User/"
            if is_macos():
                args.user_dir = f"{HOME}/Library/Application Support/Code/User/"
        os.makedirs(args.user_dir, exist_ok=True)
        shutil.copy2(src_file, args.user_dir)


def _visual_studio_code_args(subparser) -> None:
    subparser.add_argument(
        "--user-dir",
        "-d",
        dest="user_dir",
        default="",
        help="Configuration directory."
    )
    option_pip_bundle(subparser)


def _add_subparser_visual_studio_code(subparsers) -> None:
    add_subparser(
        subparsers,
        "Visual Studio Code",
        func=visual_studio_code,
        aliases=["vscode", "code"],
        add_argument=_visual_studio_code_args
    )


def intellij_idea_scala(args) -> None:
    """Install the Scala plugin for IntelliJ IDEA Community Edition.
    """
    url = "http://plugins.jetbrains.com/files/1347/73157/scala-intellij-bin-2019.3.17.zip"
    intellij_idea_plugin(version=args.version, url=url)


def _add_subparser_intellij_idea_scala(subparsers) -> None:
    add_subparser(
        subparsers, "IntelliJ IDEA", func=intellij_idea, aliases=["intellij", "idea"]
    )


def _add_subparser_ide(subparsers):
    _add_subparser_vim(subparsers)
    _add_subparser_neovim(subparsers)
    _add_subparser_spacevim(subparsers)
    _add_subparser_ideavim(subparsers)
    _add_subparser_visual_studio_code(subparsers)
    _add_subparser_intellij_idea_scala(subparsers)
    _add_subparser_bash_lsp(subparsers)
