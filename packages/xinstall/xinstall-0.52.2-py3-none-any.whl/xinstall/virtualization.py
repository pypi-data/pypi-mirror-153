"""Install virtualization related applications.
"""
from pathlib import Path
import logging
from .utils import (
    USER,
    run_cmd,
    add_subparser,
    is_win,
    is_macos,
    is_linux,
    is_debian_series,
    is_fedora_series,
    update_apt_source,
    brew_install_safe,
)


def virtualbox(args) -> None:
    """Install VirtualBox.

    :param args: A Namespace object containing parsed command-line options.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} virtualbox-qt", )
        elif is_macos():
            run_cmd("brew cask install virtualbox virtualbox-extension-pack")
        elif is_fedora_series():
            pass
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} virtualbox-qt", )
        elif is_macos():
            run_cmd("brew cask uninstall virtualbox virtualbox-extension-pack", )
        elif is_fedora_series():
            pass
    if args.config:
        pass


def _add_subparser_virtualbox(subparsers):
    add_subparser(subparsers, "VirtualBox", func=virtualbox, aliases=["vbox"])


def virtualbox_guest_additions(args) -> None:
    """Install VirtualBox Guest Additions in guest machine.

    :param args: A Namespace object containing parsed command-line options.
    :raises RuntimeError: If a Guest Additions path is not specified
        and it is not found at default locations.
    """
    if args.install:
        if not args.dir:
            logging.info(
                "Searching for VirtualBox Guest Additions in default locations ..."
            )
        if is_debian_series():
            try:
                args.dir = next(Path(f"/media/{USER}").glob("VBox_GAs_*"))
                logging.info("VirtualBox Guest Additions is found at {args.dir}.")
            except StopIteration:
                raise RuntimeError(  # pylint: disable=W0707
                    "No VirtualBox Guest Additions is found. Please specify its location manually."
                )
            cmd = f"""{args.prefix} apt-get update \
                && {args.prefix} apt-get install {args.yes_s} gcc make \
                && {args.prefix} {args.dir}/VBoxLinuxAdditions.run
                """
            run_cmd(cmd)
        elif is_fedora_series():
            pass
        elif is_macos():
            pass
    if args.uninstall:
        pass
    if args.config:
        pass


def _add_subparser_virtualbox_guest_additions(subparsers):
    add_subparser(
        subparsers,
        "VirtualBox Guest Additions",
        func=virtualbox_guest_additions,
        aliases=["vbox_ga", "vboxga"]
    )


def docker(args):
    """Install and configure Docker container.

    :param args: A Namespace object containing parsed command-line options.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            run_cmd(
                f"{args.prefix} apt-get install {args.yes_s} docker.io docker-compose"
            )
        elif is_macos():
            brew_install_safe([
                "docker",
                "docker-compose",
                "bash-completion@2",
            ])
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum install docker docker-compose")
    if args.config:
        if args.user_to_docker:
            if is_debian_series():
                run_cmd(f"{args.prefix} gpasswd -a {args.user_to_docker} docker")
                logging.warning(
                    "Please run the command 'newgrp docker' or logout/login"
                    " to make the group 'docker' effective!"
                )
            elif is_macos():
                cmd = f"{args.prefix} dseditgroup -o edit -a {args.user_to_docker} -t user staff"
                run_cmd(cmd)
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} docker docker-compose", )
        elif is_macos():
            run_cmd(
                "brew uninstall docker docker-completion docker-compose docker-compose-completion",
            )
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum remove docker docker-compose")


def _docker_args(subparser):
    subparser.add_argument(
        "--user-to-docker",
        dest="user_to_docker",
        default="" if USER == "root" else USER,
        help="The user to add to the docker group.",
    )


def _add_subparser_docker(subparsers):
    add_subparser(
        subparsers,
        "Docker",
        func=docker,
        add_argument=_docker_args,
        aliases=["dock", "dk"]
    )


def kubectl(args):
    """Install and configure the kubernetes command-line interface kubectl.

    :param args: A Namespace object containing parsed command-line options.
    """
    if args.install:
        if is_debian_series():
            run_cmd(
                f"""{args.prefix} curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg \
                && echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | {args.prefix} tee /etc/apt/sources.list.d/kubernetes.list
                """,
            )
            update_apt_source(prefix=args.prefix, seconds=-1E10)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} kubectl")
        elif is_macos():
            brew_install_safe(["kubernetes-cli"])
        elif is_fedora_series():
            pass
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} kubectl")
        elif is_macos():
            run_cmd("brew uninstall kubectl")
        elif is_fedora_series():
            pass


def _add_subparser_kubectl(subparsers):
    add_subparser(subparsers, "kubectl", func=kubectl, aliases=["k8s-cli"])


def _minikube_linux(args):
    url = "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64"
    run_cmd(
        f"""curl -L {url} -o /tmp/minikube-linux-amd64 \
            && {args.prefix} apt-get install {args.yes_s} \
                /tmp/minikube-linux-amd64 /usr/local/bin/minikube""",
    )
    print("VT-x/AMD-v virtualization must be enabled in BIOS.")


def minikube(args) -> None:
    """Install MiniKube.

    :param args: A Namespace object containing parsed command-line options.
    """
    virtualbox(args)
    kubectl(args)
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix, seconds=-1E10)
            _minikube_linux(args)
        elif is_macos():
            run_cmd("brew install minikube")
        elif is_fedora_series():
            _minikube_linux(args)
        elif is_win():
            run_cmd("choco install minikube")
            print("VT-x/AMD-v virtualization must be enabled in BIOS.")
    if args.config:
        pass
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} rm /usr/local/bin/minikube")
        elif is_macos():
            run_cmd("brew cask uninstall minikube")
        elif is_fedora_series():
            run_cmd(f"{args.prefix} rm /usr/local/bin/minikube")


def _add_subparser_minikube(subparsers):
    add_subparser(subparsers, "Minikube", func=minikube, aliases=["mkb"])


def multipass(args) -> None:
    """Install Multipass.

    :param args: A Namespace object containing parsed command-line options.
    """
    if args.install:
        if is_debian_series():
            cmd = f"{args.prefix} snap install multipass --classic"
            run_cmd(cmd)
        elif is_macos():
            cmd = "brew cask install multipass"
            run_cmd(cmd)
        elif is_fedora_series():
            pass
        elif is_win():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_debian_series():
            cmd = f"{args.prefix} snap uninstall multipass"
            run_cmd(cmd)
        elif is_macos():
            run_cmd("brew cask uninstall multipass")
        elif is_fedora_series():
            pass


def _add_subparser_multipass(subparsers):
    add_subparser(subparsers, "Multipass", func=multipass, aliases=["mp"])


def microk8s(args) -> None:
    """Install and configure MicroK8S.
    Note that snap must be available in order to install microk8s.

    :param args: A Namespace object containing parsed command-line options.
    """
    if args.install:
        if is_linux():
            cmd = f"""{args.prefix} snap install microk8s --classic \
                    && {args.prefix} ln -svf /snap/bin/microk8s.kubectl /snap/bin/kubectl \
                    && {args.prefix} gpasswd -a $(id -un) microk8s"""
            run_cmd(cmd)
        elif is_macos():
            pass
        elif is_win():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_debian_series():
            cmd = f"{args.prefix} snap uninstall microk8s"
            run_cmd(cmd)
        elif is_macos():
            pass
        elif is_fedora_series():
            pass


def _add_subparser_microk8s(subparsers):
    add_subparser(subparsers, "Microk8s", func=microk8s, aliases=["mk8s"])


def _add_subparser_virtualization(subparsers):
    _add_subparser_docker(subparsers)
    _add_subparser_kubectl(subparsers)
    _add_subparser_minikube(subparsers)
    _add_subparser_virtualbox(subparsers)
    _add_subparser_multipass(subparsers)
    _add_subparser_microk8s(subparsers)
