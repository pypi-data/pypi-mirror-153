"""Installing dev related tools.
"""
import os
import logging
import shutil
from pathlib import Path
import re
import urllib.request
from argparse import Namespace
import tomlkit
from .utils import (
    HOME,
    BASE_DIR,
    is_debian_series,
    is_fedora_series,
    is_linux,
    update_apt_source,
    brew_install_safe,
    is_macos,
    is_win,
    remove_file_safe,
    run_cmd,
    add_subparser,
    option_version,
    option_pip_bundle,
    option_python,
    update_file,
    update_dict,
)
from .network import ssh_client


def openjdk8(args):
    """Install OpenJDK 8.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            run_cmd(
                f"{args.prefix} apt-get install {args.yes_s} openjdk-jdk-8 maven gradle"
            )
        if is_macos():
            cmd = "brew tap AdoptOpenJDK/openjdk && brew cask install adoptopenjdk8"
            run_cmd(cmd)
        if is_fedora_series():
            pass
    if args.uninstall:
        if is_debian_series():
            run_cmd(
                f"{args.prefix} apt-get purge {args.yes_s} openjdk-jdk-8 maven gradle"
            )
        if is_macos():
            run_cmd("brew cask uninstall adoptopenjdk8")
        if is_fedora_series():
            pass


def _add_subparser_openjdk(subparsers):
    add_subparser(subparsers, "OpenJDK8", func=openjdk8, aliases=["jdk8"])


def sdkman(args):
    """ Install sdkman.
    https://sdkman.io/install
    """
    if args.install:
        run_cmd("curl -s https://get.sdkman.io | bash")
    if args.config:
        pass
    if args.uninstall:
        pass


def _add_subparser_sdkman(subparsers):
    add_subparser(subparsers, "sdkman", func=sdkman, aliases=[])


def yapf(args):
    """Install Google's yapf (for formatting Python scripts).
    """
    if args.install:
        run_cmd(f"{args.pip_install} yapf")
    if args.config:
        # configure yapf formatting via pyproject.toml
        src_file = BASE_DIR / "yapf/pyproject.toml"
        dic_src = tomlkit.loads(src_file.read_text())
        des_file = args.dst_dir / "pyproject.toml"
        if des_file.is_file():
            dic_des = tomlkit.loads(des_file.read_text())
        else:
            dic_des = {}
        update_dict(dic_des, dic_src, recursive=True)
        des_file.write_text(tomlkit.dumps(dic_des))
        logging.info("yapf is configured via %s.", des_file)
    if args.uninstall:
        run_cmd(f"{args.pip_uninstall} yapf")


def _yapf_args(subparser):
    subparser.add_argument(
        "-d",
        "--dest-dir",
        dest="dst_dir",
        type=Path,
        default=Path(),
        help="The destination directory to copy the YAPF configuration file to.",
    )
    option_pip_bundle(subparser)


def _add_subparser_yapf(subparsers):
    add_subparser(subparsers, "yapf", func=yapf, aliases=[], add_argument=_yapf_args)


def pylint(args):
    """Install and configure pylint.
    """
    if args.install:
        run_cmd(f"{args.pip_install} pylint")
    if args.config:
        src_file = BASE_DIR / "pylint/pyproject.toml"
        dic_src = tomlkit.loads(src_file.read_text())
        des_file = args.dst_dir / "pyproject.toml"
        if des_file.is_file():
            dic_des = tomlkit.loads(des_file.read_text())
        else:
            dic_des = {}
        update_dict(dic_des, dic_src, recursive=True)
        des_file.write_text(tomlkit.dumps(dic_des))
        logging.info("pylint is configured via %s.", des_file)
    if args.uninstall:
        run_cmd(f"{args.pip_uninstall} pylint")


def _pylint_args(subparser):
    subparser.add_argument(
        "-d",
        "--dest-dir",
        dest="dst_dir",
        type=Path,
        default=Path(),
        help="The destination directory to copy the pylint configuration file to.",
    )
    option_pip_bundle(subparser)


def _add_subparser_pylint(subparsers):
    add_subparser(
        subparsers, "pylint", func=pylint, aliases=[], add_argument=_pylint_args
    )


def flake8(args):
    """Install and configure flake8.
    """
    if args.install:
        run_cmd(f"{args.pip_install} flake8")
    if args.config:
        src_file = BASE_DIR / "flake8/flake8"
        des_file = args.dst_dir / ".flake8"
        shutil.copy2(src_file, des_file)
        logging.info("%s is copied to %s.", src_file, des_file)
    if args.uninstall:
        run_cmd(f"{args.pip_uninstall} flake8")


def _flake8_args(subparser):
    subparser.add_argument(
        "-d",
        "--dest-dir",
        dest="dst_dir",
        type=Path,
        default=Path(),
        help="The destination directory to copy the flake8 configuration file to.",
    )
    option_pip_bundle(subparser)


def _add_subparser_flake8(subparsers):
    add_subparser(
        subparsers, "flake8", func=flake8, aliases=[], add_argument=_flake8_args
    )


def darglint(args):
    """Install and configure darglint.
    """
    if args.install:
        run_cmd(f"{args.pip_install} darglint")
    if args.config:
        src_file = BASE_DIR / "darglint/darglint"
        des_file = args.dst_dir / ".darglint"
        shutil.copy2(src_file, des_file)
        logging.info("%s is copied to %s.", src_file, des_file)
    if args.uninstall:
        run_cmd(f"{args.pip_uninstall} darglint")


def _darglint_args(subparser):
    subparser.add_argument(
        "-d",
        "--dest-dir",
        dest="dst_dir",
        type=Path,
        default=Path(),
        help="The destination directory to copy the darglint configuration file to.",
    )
    option_pip_bundle(subparser)


def _add_subparser_darglint(subparsers):
    add_subparser(
        subparsers, "darglint", func=darglint, aliases=[], add_argument=_darglint_args
    )


def pytype(args):
    """Install and configure pytype.
    """
    if args.install:
        run_cmd(f"{args.pip_install} pytype")
    if args.config:
        src_file = BASE_DIR / "pytype/setup.cfg"
        des_file = args.dst_dir / "setup.cfg"
        shutil.copy2(src_file, des_file)
        logging.info("%s is copied to %s.", src_file, des_file)
    if args.uninstall:
        run_cmd(f"{args.pip_uninstall} pytype")


def _pytype_args(subparser):
    subparser.add_argument(
        "-d",
        "--dest-dir",
        dest="dst_dir",
        type=Path,
        default=Path(),
        help="The destination directory to copy the pytype configuration file to.",
    )
    option_pip_bundle(subparser)


def _add_subparser_pytype(subparsers):
    add_subparser(
        subparsers, "pytype", func=pytype, aliases=[], add_argument=_pytype_args
    )


def nodejs(args):
    """Install nodejs and npm.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            cmd = f"{args.prefix} apt-get install {args.yes_s} nodejs npm"
            run_cmd(cmd)
        if is_macos():
            brew_install_safe(["node"])
        if is_fedora_series():
            run_cmd(f"{args.prefix} yum install {args.yes_s} nodejs")
    if args.config:
        pass
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} nodejs")
        if is_macos():
            run_cmd("brew uninstall nodejs")
        if is_fedora_series():
            run_cmd(f"{args.prefix} yum remove nodejs")


def _add_subparser_nodejs(subparsers):
    add_subparser(subparsers, "NodeJS", func=nodejs, aliases=["node"])


def python(args):
    """Install and configure Python (3).
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            cmd = f"""{args.prefix} apt-get install {args.yes_s} \
                python3 python3-dev python3-pip python3-setuptools python3-venv"""
            run_cmd(cmd)
        if is_macos():
            brew_install_safe(["python3"])
        if is_fedora_series():
            run_cmd(
                f"""{args.prefix} yum install {args.yes_s} \
                python3 python3-devel python3-pip"""
            )
            run_cmd(f"{args.pip_install} setuptools")
    if args.config:
        if not shutil.which("python"):
            python3 = shutil.which("python3")
            if python3:
                Path(python3[:-1]).symlink_to(python3)
    if args.uninstall:
        if is_debian_series():
            cmd = f"""{args.prefix} apt-get purge {args.yes_s} \
                python3 python3-dev python3-setuptools python3-pip python3-venv"""
            run_cmd(cmd)
        if is_macos():
            run_cmd("brew uninstall python3")
        if is_fedora_series():
            run_cmd(f"{args.prefix} yum remove python3")


def _python_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_python3(subparsers):
    add_subparser(
        subparsers,
        "Python",
        func=python,
        aliases=["py", "py3", "python3"],
        add_argument=_python_args
    )


def poetry(args):
    """Install and configure Python poetry.
    """
    if args.install:
        url = "https://install.python-poetry.org"
        cmd = f"curl -sSL {url} | {args.python}"
        if args.version:
            cmd += f" - --version {args.version}"
        run_cmd(cmd)
    poetry_bin = HOME / ".local/bin/poetry"
    if args.config:
        # make poetry always create virtual environment in the root directory of the project
        run_cmd(f"{poetry_bin} config virtualenvs.in-project true")
        logging.info(
            "Python poetry has been configured to create virtual environments inside projects!"
        )
        # bash completion
        if args.bash_completion:
            if is_linux():
                cmd = f"""{poetry_bin} completions bash | tee \
                    /etc/bash_completion.d/poetry.bash-completion > /dev/null"""
                run_cmd(cmd)
                return
            if is_macos():
                cmd = f"""{poetry_bin} completions bash > \
                    $(brew --prefix)/etc/bash_completion.d/poetry.bash-completion"""
                run_cmd(cmd)
            logging.info("Bash completion is enabled for poetry.")
    if args.uninstall:
        run_cmd(f"{poetry_bin} self:uninstall")


def _poetry_args(subparser):
    subparser.add_argument(
        "-b",
        "--bash-completion",
        dest="bash_completion",
        action="store_true",
        help="Configure Bash completion for poetry as well."
    )
    option_version(subparser, help="The version of Python Poetry to install.")
    option_python(subparser)


def _add_subparser_poetry(subparsers):
    add_subparser(
        subparsers, "Poetry", func=poetry, aliases=["pt"], add_argument=_poetry_args
    )


def pyjnius(args):
    """Install pyjnius for calling Java from Python.
    """
    if args.install:
        cmd = f"{args.pip_install} Cython pyjnius"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _pyjnius_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_pyjnius(subparsers):
    add_subparser(
        subparsers,
        "pyjnius",
        func=pyjnius,
        aliases=["pyj"],
        add_argument=_pyjnius_args
    )


def rustup(args):
    """Install rustup which is the version management tool for Rust.
    """
    if args.install:
        if is_win():
            pass
        else:
            cmd = """curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y \
                && ~/.cargo/bin/rustup component add rust-src rustfmt clippy \
                && ~/.cargo/bin/cargo install sccache cargo-cache
                """
            run_cmd(cmd)
        if is_debian_series():
            cmd = f"""{args.prefix} apt-get update \
                    && {args.prefix} apt-get install -y cmake libssl-dev pkg-config
                """
            run_cmd(cmd)
        run_cmd("~/.cargo/bin/cargo install cargo-edit")
    if args.config:
        _link_rust(args)
    if args.uninstall:
        cmd = "~/.cargo/bin/rustup self uninstall"
        run_cmd(cmd)


def _rustup_args(subparser):
    subparser.add_argument(
        "--link-to-dir",
        dest="link_to_dir",
        default="",
        help="The directory to link commands (cargo and rustc) to."
    )


def _link_rust(args) -> None:
    if not args.link_to_dir:
        return
    home_cargo_bin = HOME / ".cargo/bin"
    if is_win():
        return
    for cmd in ["rustup", "cargo", "rustc"]:
        run_cmd(f"{args.prefix} ln -svf {home_cargo_bin / cmd} {args.link_to_dir}/")


def _add_subparser_rustup(subparsers):
    add_subparser(
        subparsers,
        "rustup",
        func=rustup,
        aliases=["rust", "cargo"],
        add_argument=_rustup_args
    )


def rustpython(args):
    """Install and configure RustPython.
    """
    rustup(args)
    if args.install:
        cmd = "/root/.cargo/bin/cargo install rustpython"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = "/root/.cargo/bin/cargo uninstall rustpython"
        run_cmd(cmd)


def _add_subparser_rustpython(subparsers):
    add_subparser(subparsers, "RustPython", func=rustpython, aliases=["rustpy"])


def flamegraph(args):
    """Install and configure FlameGraph.
    """
    if args.install:
        if is_debian_series():
            logging.info("Installing FlameGraph ...")
            cmd = f"""{args.prefix} apt-get update \
                && {args.prefix} apt-get install {args.yes_s} \
                    linux-tools-common \
                    linux-tools-generic \
                    linux-tools-`uname -r` \
                && cargo install flamegraph"""
            run_cmd(cmd)
        else:
            raise NotImplementedError(
                "Installing FlameGraph is not supported on this OS."
            )
    if args.config:
        pass
    if args.uninstall:
        pass


def _add_subparser_flamegraph(subparsers):
    add_subparser(
        subparsers,
        "flamegraph",
        func=flamegraph,
        aliases=["flame", "flameg", "fgraph", "fg"],
    )


def _git_ignore(args: Namespace) -> None:
    """Insert patterns to ingore into .gitignore in the current directory.
    """
    if not args.language:
        return
    srcfile = BASE_DIR / f"git/gitignore_{args.language}"
    dstfile = args.dst_dir / ".gitignore"
    mode = "a" if args.append else "w"
    with dstfile.open(mode) as fout:
        fout.write(srcfile.read_text())
    msg = f"%s is {'appended into' if mode == 'a' else 'copied to'} %s."
    logging.info(msg, srcfile, dstfile)


def git_(args) -> None:
    """Install and configure Git.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} git git-lfs")
        elif is_macos():
            brew_install_safe(["git", "git-lfs", "bash-completion@2"])
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum install git")
        run_cmd("git lfs install")
    if args.uninstall:
        run_cmd("git lfs uninstall")
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} git git-lfs")
        elif is_macos():
            run_cmd("brew uninstall git git-lfs")
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum remove git")
    if args.config:
        ssh_client(args)
        gitconfig = HOME / ".gitconfig"
        # try to remove the file to avoid dead symbolic link problem
        remove_file_safe(gitconfig)
        shutil.copy2(BASE_DIR / "git/gitconfig", gitconfig)
        logging.info("%s is copied to %s", BASE_DIR / "git/gitconfig", gitconfig)
        if is_macos():
            file = "/usr/local/etc/bash_completion.d/git-completion.bash"
            bashrc = f"\n# Git completion\n[ -f {file} ] &&  . {file}"
            with (HOME / ".bash_profile").open("a") as fout:
                fout.write(bashrc)
            logging.info("Bash completion is enabled for Git.")
    _git_ignore(args)
    if "proxy" in args and args.proxy:
        run_cmd(f"git config --global http.proxy {args.proxy}")
        run_cmd(f"git config --global https.proxy {args.proxy}")


def _git_args(subparser):
    subparser.add_argument(
        "--proxy",
        dest="proxy",
        default="",
        help="Configure Git to use the specified proxy."
    )
    subparser.add_argument(
        "-d",
        "--dest-dir",
        dest="dst_dir",
        type=Path,
        default=Path(),
        help="The destination directory to copy the YAPF configuration file to.",
    )
    subparser.add_argument(
        "-p",
        "--python",
        dest="language",
        action="store_const",
        const="python",
        default="",
        help="Gitignore patterns for Python developing."
    )
    subparser.add_argument(
        "-j",
        "--java",
        dest="language",
        action="store_const",
        const="java",
        help="Gitignore patterns for Java developing."
    )
    subparser.add_argument(
        "-r",
        "--rust",
        dest="language",
        action="store_const",
        const="rust",
        help="Gitignore patterns for Rust developing."
    )
    subparser.add_argument(
        "-a",
        "--append",
        dest="append",
        action="store_true",
        help="Append patterns to ignore into .gitignore rather than overwrite it."
    )


def _add_subparser_git(subparsers):
    add_subparser(subparsers, "Git", func=git_, add_argument=_git_args)


def antlr(args):
    """Install and configure Antrl4.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} antlr4")
        elif is_macos():
            brew_install_safe(["antlr4"])
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum install antlr")
    if args.config:
        pass
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} antlr4")
        elif is_macos():
            run_cmd("brew uninstall antlr4")
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum remove antlr")


def _add_subparser_antlr(subparsers):
    add_subparser(subparsers, "ANTLR", func=antlr)


def jpype1(args):
    """Install the Python package JPype.
    """
    if args.install:
        cmd = f"{args.pip_install} JPype1"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip_uninstall} JPype1"
        run_cmd(cmd)


def _jpype1_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_jpype1(subparsers):
    add_subparser(
        subparsers,
        "JPype1",
        func=jpype1,
        aliases=["jpype", "jp"],
        add_argument=_jpype1_args
    )


def deno(args):
    """Install and configure Deno.

    :param args:
    """
    if args.install:
        cmd = "curl -fsSL https://deno.land/x/install/install.sh | sh"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _add_subparser_deno(subparsers):
    add_subparser(subparsers, "Deno", func=deno, aliases=[])


def sphinx(args):
    """Install and configure Sphinx.

    :param args:
    """
    if args.install:
        cmd = f"{args.pip_install} sphinx sphinx-autodoc-typehints"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip_uninstall} sphinx sphinx-autodoc-typehints"
        run_cmd(cmd)


def _sphinx_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_sphinx(subparsers):
    add_subparser(
        subparsers, "sphinx", func=sphinx, aliases=[], add_argument=_sphinx_args
    )


def pyenv(args):
    """Install and configure pyenv.
    """
    if not (args.root.endswith("pyenv") or args.root.endswith(".pyenv")):
        args.root = os.path.join(args.root, "pyenv")
    if args.install:
        if is_win():
            raise NotImplementedError(
                "The subcommand 'xinstall pyenv' is not implemented for Windows yet!"
            )
        if is_macos():
            cmd = "brew install pyenv"
            run_cmd(cmd)
        else:
            logging.info("Installing pyenv ...")
            cmd = f"""{args.prefix} rm -rf {args.root} && curl -sSL https://pyenv.run \
                | PYENV_ROOT={args.root} bash"""
            run_cmd(cmd)
            if is_debian_series():
                logging.info(
                    "Installing header files (for building Python and Python packages) ..."
                )
                update_apt_source(prefix=args.prefix, seconds=1E-10)
                cmd = f"""{args.prefix} apt-get install {args.yes_s} \
                    libssl-dev libbz2-dev libreadline-dev libsqlite3-dev libffi-dev liblzma-dev
                    """
                run_cmd(cmd)
    if args.config:
        update_file(
            HOME / ".bashrc",
            append=[
                "\n\n# PyEnv",
                f'export PATH="{args.root}/bin:$PATH"',
                'eval "$(pyenv init -)"',
                'eval "$(pyenv virtualenv-init -)"\n',
            ]
        )
        logging.info("PyEnv has been configured for bash.")
    if args.uninstall:
        run_cmd(f"rm -rf {args.root}")
        update_file(
            HOME / ".bashrc",
            exact=[
                ("# PyEnv", ""),
                (f'export PATH="{args.root}/bin:$PATH"\n', ""),
                ('eval "$(pyenv init -)"\n', ""),
                ('eval "$(pyenv virtualenv-init -)"\n', ""),
            ]
        )


def _pyenv_args(subparser):
    subparser.add_argument(
        "-r",
        "-d",
        "--root",
        "--pyenv-root",
        dest="root",
        default=os.environ.get("PYENV_ROOT", str(HOME / ".pyenv")),
        help=
        "The root directory for installing PyEnv, e.g., `/opt/pyenv` or `/home/dclong/.pyenv`."
    )


def _add_subparser_pyenv(subparsers):
    add_subparser(
        subparsers,
        "pyenv",
        func=pyenv,
        aliases=[],
        add_argument=_pyenv_args,
    )


def jenv(args):
    """Install and configure jEnv.
    """
    if not (args.root.endswith("jenv") or args.root.endswith(".jenv")):
        args.root = os.path.join(args.root, "jenv")
    if args.install:
        if is_win():
            raise NotImplementedError(
                "The subcommand 'xinstall jenv' is not implemented for Windows yet!"
            )
        if is_macos():
            cmd = "brew install jenv"
            run_cmd(cmd)
        else:
            logging.info("Installing jenv ...")
            cmd = f"""{args.prefix} rm -rf {args.root} \
                && git clone https://github.com/jenv/jenv.git ~/.jenv
                """
            run_cmd(cmd)
    if args.config:
        update_file(
            HOME / ".bashrc",
            append=[
                "\n\n# jEnv",
                f'export PATH="{args.root}/bin:$PATH"',
                'eval "$(jenv init -)"',
            ]
        )
        logging.info("jEnv has been configured for bash.")
    if args.uninstall:
        run_cmd(f"rm -rf {args.root}")
        update_file(
            HOME / ".bashrc",
            exact=[
                ("# jEnv", ""),
                (f'export PATH="{args.root}/bin:$PATH"\n', ""),
                ('eval "$(jenv init -)"\n', ""),
            ]
        )


def _jenv_args(subparser):
    subparser.add_argument(
        "-r",
        "-d",
        "--root",
        "--jenv-root",
        dest="root",
        default=os.environ.get("JENV_ROOT", str(HOME / ".pyenv")),
        help=
        "The root directory for installing jEnv, e.g., `/opt/pyenv` or `/home/dclong/.pyenv`."
    )


def _add_subparser_jenv(subparsers):
    add_subparser(
        subparsers,
        "jenv",
        func=jenv,
        aliases=[],
        add_argument=_jenv_args,
    )


def _parse_golang_version():
    url = "https://github.com/golang/go/tags"
    with urllib.request.urlopen(url) as fin:
        html = fin.read().decode()
    pattern = r"tag/go(\d+\.\d+\.\d+)"
    match = re.search(pattern, html)
    if not match:
        raise RuntimeError(
            f"The pattern {pattern} is not found in the source HTML code of the page {url}!"
        )
    return match.groups(0)[0]


def golang(args):
    """Install and configure GoLANG.
    """
    if args.install:
        logging.info("Installing GoLANG ...")
        if is_linux():
            ver = _parse_golang_version()
            cmd = f"""curl -sSL https://go.dev/dl/go{ver}.linux-amd64.tar.gz -o /tmp/go.tar.gz \
                    && {args.prefix} rm -rf /usr/local/go \
                    && {args.prefix} tar -C /usr/local/ -xzf /tmp/go.tar.gz
                """
            run_cmd(cmd)
        elif is_macos():
            brew_install_safe("go")
        elif is_win():
            pass
    if args.config:
        if is_linux():
            usr_local_bin = Path("/usr/local/bin/")
            for path in Path("/usr/local/go/bin/").iterdir():
                logging.info(
                    "Creating a symbolic link of %s into %s/ ...", path, usr_local_bin
                )
                cmd = f"{args.prefix} ln -svf {path} {usr_local_bin}/"
                run_cmd(cmd)
        elif is_macos():
            pass
        else:
            pass
    if args.uninstall:
        pass


def _add_subparser_golang(subparsers):
    add_subparser(subparsers, "GoLANG", func=golang, aliases=["go"])


def cmake(args):
    """Install and configure cmake.
    """
    if args.install:
        logging.info("Installing cmake ...")
        if is_debian_series():
            update_apt_source(prefix=args.prefix, seconds=1E-10)
            cmd = f"{args.prefix} apt-get install {args.yes_s} cmake"
            run_cmd(cmd)
        elif is_macos():
            brew_install_safe("cmake")
        elif is_win():
            pass
    if args.uninstall:
        if is_debian_series():
            cmd = f"{args.prefix} apt-get purge {args.yes_s} cmake"
            run_cmd(cmd)
        elif is_macos():
            run_cmd("brew uninstall cmake")
        elif is_win():
            pass


def _add_subparser_cmake(subparsers):
    add_subparser(
        subparsers,
        "cmake",
        func=cmake,
    )


def _add_subparser_dev(subparsers):
    _add_subparser_cmake(subparsers)
    _add_subparser_git(subparsers)
    _add_subparser_nodejs(subparsers)
    _add_subparser_python3(subparsers)
    _add_subparser_golang(subparsers)
    _add_subparser_sphinx(subparsers)
    _add_subparser_pyjnius(subparsers)
    _add_subparser_yapf(subparsers)
    _add_subparser_pylint(subparsers)
    _add_subparser_flake8(subparsers)
    _add_subparser_darglint(subparsers)
    _add_subparser_pytype(subparsers)
    _add_subparser_pyenv(subparsers)
    _add_subparser_jenv(subparsers)
    _add_subparser_openjdk(subparsers)
    _add_subparser_sdkman(subparsers)
    _add_subparser_poetry(subparsers)
    _add_subparser_rustup(subparsers)
    _add_subparser_flamegraph(subparsers)
    _add_subparser_rustpython(subparsers)
    _add_subparser_deno(subparsers)
    _add_subparser_antlr(subparsers)
    _add_subparser_jpype1(subparsers)
