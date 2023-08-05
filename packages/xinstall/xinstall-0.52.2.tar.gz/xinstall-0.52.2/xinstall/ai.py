"""Install AI related tools.
"""
from pathlib import Path
import logging
from .utils import (
    HOME, USER, run_cmd, add_subparser, is_debian_series, is_macos, is_win,
    option_pip_bundle
)


def _add_subparser_ai(subparsers):
    _add_subparser_kaggle(subparsers)
    _add_subparser_lightgbm(subparsers)
    _add_subparser_pytorch(subparsers)
    _add_subparser_autogluon(subparsers)
    _add_subparser_pytext(subparsers)
    _add_subparser_computer_vision(subparsers)
    _add_subparser_nlp(subparsers)
    _add_subparser_heic(subparsers)


def kaggle(args):
    """Install the Python package kaggle.
    """
    if args.install:
        cmd = f"{args.pip_install} kaggle"
        run_cmd(cmd)
    if args.config:
        home_host = Path(f"/home_host/{USER}/")
        kaggle_home_host = home_host / ".kaggele"
        kaggle_home = HOME / ".kaggele"
        if home_host.is_dir():
            kaggle_home_host.mkdir(exist_ok=True)
            try:
                kaggle_home.symlink_to(kaggle_home_host)
                logging.info(
                    "Symbolic link %s pointing to %s is created.", kaggle_home,
                    kaggle_home_host
                )
            except FileExistsError:
                pass
        else:
            kaggle_home.mkdir(exist_ok=True)
            logging.info("The directory %s is created.", kaggle_home)
    if args.uninstall:
        pass


def _kaggle_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_kaggle(subparsers):
    add_subparser(
        subparsers, "kaggle", func=kaggle, aliases=[], add_argument=_kaggle_args
    )


def lightgbm(args):
    """Install the Python package kaggle.
    """
    if args.install:
        cmd = f"""{args.pip_install} lightgbm scikit-learn pandas matplotlib scipy graphviz"""
        run_cmd(cmd)


def _lightgbm_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_lightgbm(subparsers):
    add_subparser(
        subparsers, "lightgbm", func=lightgbm, aliases=[], add_argument=_lightgbm_args
    )


def pytorch(args):
    """Install PyTorch.
    """
    if args.install:
        version = "cu" + args.cuda_version.replace(
            ".", ""
        ) if args.cuda_version else "cpu"
        cmd = f"{args.pip_install} torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/{version}"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _pytorch_args(subparser):
    subparser.add_argument(
        "--cuda-version",
        "--cuda",
        dest="cuda_version",
        default="",
        help="The version of CUDA. If not specified, the CPU version is used."
    )
    option_pip_bundle(subparser)


def _add_subparser_pytorch(subparsers):
    add_subparser(
        subparsers, "PyTorch", func=pytorch, aliases=[], add_argument=_pytorch_args
    )


def autogluon(args):
    """Install the Python package AutoGluon.
    """
    if args.install:
        cmd = f"{args.pip_install} 'mxnet<2.0.0' autogluon"
        if args.cuda_version:
            version = args.cuda_version.replace(".", "")
            cmd = f"{args.pip_install} 'mxnet-cu{version}<2.0.0' autogluon"
        run_cmd(cmd)


def _autogluon_args(subparser):
    subparser.add_argument(
        "--cuda",
        "--cuda-version",
        dest="cuda_version",
        required=True,
        help="If a valid version is specified, "
        "install the GPU version of AutoGluon with the specified version of CUDA."
    )
    option_pip_bundle(subparser)


def _add_subparser_autogluon(subparsers):
    add_subparser(
        subparsers,
        "AutoGluon",
        func=autogluon,
        aliases=[],
        add_argument=_autogluon_args,
    )


def pytext(args):
    """Install the Python package PyText.
    """
    if args.install:
        cmd = f"{args.pip_install} pytext-nlp"
        if args.cuda_version:
            pass
        run_cmd(cmd)


def _pytext_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_pytext(subparsers):
    add_subparser(subparsers, "pytext", func=pytext, add_argument=_pytext_args)


def computer_vision(args):
    """Install computer vision Python packages: opencv-python, scikit-image and Pillow.
    """
    if args.install:
        if is_debian_series():
            cmd = f"""{args.prefix} apt-get update \
                    && {args.prefix} apt-get install {args.yes_s} \
                        libsm6 libxrender-dev libaec-dev libxext6 \
                        libblosc-dev libbrotli-dev libghc-bzlib-dev libgif-dev \
                        libopenjp2-7-dev liblcms2-dev libjxr-dev liblz4-dev \
                        liblzma-dev libpng-dev libsnappy-dev libtiff-dev \
                        libwebp-dev libzopfli-dev libzstd-dev \
                        ffmpeg \
                    && {args.pip_install} opencv-python scikit-image pillow"""
            run_cmd(cmd)
        elif is_macos():
            cmd = f"""{args.pip_install} opencv-python scikit-image pillow"""
            run_cmd(cmd)


def _computer_vision_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_computer_vision(subparsers):
    add_subparser(
        subparsers,
        "computer_vision",
        func=computer_vision,
        aliases=["vision", "cv"],
        add_argument=_computer_vision_args
    )


def heic(args):
    """Install HEIC related libraries and tools.
    """
    if args.install:
        if is_debian_series():
            cmd = f"""{args.prefix} apt-get update \
                    && {args.prefix} apt-get install {args.yes_s} \
                        heif-gdk-pixbuf libheif-examples
                    """
            run_cmd(cmd)
        elif is_win():
            pass
        elif is_macos():
            pass
    if args.config:
        pass
    if args.uninstall:
        pass


def _add_subparser_heic(subparsers):
    add_subparser(
        subparsers,
        "heic",
        func=heic,
        aliases=["heif"],
    )


def nlp(args):
    """Install Python packages (PyTorch, transformers, pytext-nlp and fasttext) for NLP.
    """
    if args.install:
        cmd = f"""{args.pip_install} torch torchvision transformers pytext-nlp fasttext"""
        run_cmd(cmd)


def _nlp_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_nlp(subparsers):
    add_subparser(subparsers, "nlp", func=nlp, add_argument=_nlp_args)


def cuda(args):
    """Install CUDA for GPU computing.
    """
    if args.install:
        if is_debian_series():
            pkgs = "cuda" if args.full else "cuda-drivers"
            cmd = f"""wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin -O /tmp/cuda-ubuntu2004.pin \
                && {args.prefix} mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600 \
                {args.prefix} apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub \
                {args.prefix} add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
                {args.prefix} apt-get update \
                {args.prefix} apt-get {args.yes_s} install {pkgs}
                """
            run_cmd(cmd)
            logging.info(
                "The package(s) %s have been installed. \nYou might have to restart your computer for it to take effect!",
                pkgs
            )
        elif is_win():
            pass
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.prefix} apt-get {args.yes_s} purge cuda-drivers"
        run_cmd(cmd)


def _cuda_args(subparser):
    subparser.add_argument(
        "--full",
        dest="full",
        action="store_true",
        help=
        "Install the package cuda (full installation) instead of cuda-drivers (drivers only)."
    )


def _add_subparser_cuda(subparsers):
    add_subparser(subparsers, "cuda", func=cuda, add_argument=_cuda_args)


def nvidia_docker(args):
    """Install nvidia-docker2 (on a  Linux machine).
    """
    if args.install:
        if is_debian_series():
            cmd = f"""distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
                    && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
                    && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list \
                    && {args.prefix} apt-get update \
                    && {args.prefix} apt-get install -y nvidia-docker2
                """
            run_cmd(cmd)
            logging.info(
                "The package nvidia-docker2 has been installed. \nPlease restart Docker (sudo service docker restart)."
            )
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.prefix} apt-get {args.yes_s} purge nvidia-docker2"
        run_cmd(cmd)


def _add_subparser_nvidia_docker(subparsers):
    add_subparser(subparsers, "nvidia_docker", func=nvidia_docker)


def pandas(args):
    """Install Python pandas and related packages.

    :param args: A Namespace object containing parsed command-line options.
    """
    if args.install:
        cmd = f"{args.pip_install} pandas pyarrow"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip_uninstall} pandas pyarrow"
        run_cmd(cmd)


def _add_subparser_pandas(subparsers):
    add_subparser(subparsers, "pandas", func=pandas)


def python_visualization(args):
    """Install Python visualization packages.

    :param args: A Namespace object containing parsed command-line options.
    """
    if args.install:
        cmd = f"{args.pip_install} hvplot matplotlib"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip_uninstall} hvplot matplotlib"
        run_cmd(cmd)


def _add_subparser_python_visualization(subparsers):
    add_subparser(
        subparsers,
        "Python visualization packages",
        func=python_visualization,
        aliases=["pyvis"]
    )
