# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xinstall',
 'xinstall.data.ipython',
 'xinstall.data.jupyter',
 'xinstall.data.linux.autokey.data.Sample Scripts']

package_data = \
{'': ['*'],
 'xinstall': ['data/SpaceVim/SpaceVim.d/*',
              'data/SpaceVim/SpaceVim/*',
              'data/chrome/vimium/*',
              'data/cygwin/*',
              'data/darglint/*',
              'data/eclipse/*',
              'data/firefox/*',
              'data/firefox/noscripts/config/*',
              'data/firefox/noscripts/whitelist/*',
              'data/flake8/*',
              'data/geany/*',
              'data/geany/colorschemes/*',
              'data/geany/filedefs/*',
              'data/geany/templates/*',
              'data/git/*',
              'data/git/mac/*',
              'data/hyper/*',
              'data/intellij/*',
              'data/jupyter-book/*',
              'data/linux/*',
              'data/linux/applications/*',
              'data/linux/apt/*',
              'data/linux/autokey/data/My Phrases/*',
              'data/linux/autokey/data/My Phrases/Addresses/*',
              'data/linux/autostart/*',
              'data/linux/crontab/*',
              'data/linux/dictionary/*',
              'data/linux/docker/*',
              'data/linux/eclipse/*',
              'data/linux/gedit/*',
              'data/linux/gmail/*',
              'data/linux/jabref/*',
              'data/linux/lightdm/*',
              'data/linux/mail/*',
              'data/linux/network/*',
              'data/linux/postfix/*',
              'data/linux/r/*',
              'data/linux/remmina/*',
              'data/linux/rsnapshot/*',
              'data/linux/synaptics/*',
              'data/linux/tcpd/*',
              'data/linux/terminator/*',
              'data/linux/texlive/*',
              'data/linux/uget/*',
              'data/linux/wget/*',
              'data/linux/xdg/*',
              'data/linux/xsession/*',
              'data/ls/*',
              'data/nfs/*',
              'data/nomachine/desktop/*',
              'data/proxychains/*',
              'data/pylint/*',
              'data/pytype/*',
              'data/rstudio-desktop/*',
              'data/spark/*',
              'data/ssh/client/*',
              'data/ssh/server/*',
              'data/teamdrive/*',
              'data/tmux/*',
              'data/vscode/*',
              'data/xonsh/*',
              'data/yapf/*']}

install_requires = \
['distro>=1.5.0',
 'findspark>=1.4.2',
 'packaging>=20.4',
 'requests>=2.25.0',
 'tomlkit>=0.7.0',
 'tqdm>=4.48.2']

entry_points = \
{'console_scripts': ['xinstall = xinstall:main.main']}

setup_kwargs = {
    'name': 'xinstall',
    'version': '0.52.2',
    'description': 'Easy Cross-platform Installation and Configuration of Apps.',
    'long_description': '# [xinstall](https://github.com/legendu-net/xinstall): Easy Cross-platform Installation and Configuration of Apps\n\n## Install xinstall\n\n    :::bash\n    pip3 install -U xinstall\n\n## Usage\n\n1. Run `xinstall -h` for the help doc.\n        \n2. Below is an example of install SpaceVim and configure it.\n\n        xinstall svim -ic\n    \n3. In case `xinstall` is not on the search path, \n    you can use `python3 -m xinstall.main` instead. \n    For example, \n    to check the help doc.\n    \n        python3 -m xinstall.main -h\n        \n### sudo Permission\n\nxinstall has 3 levels of `sudo` permission.\n\n- (L1) Non-root user running `xinstall subcmd -ic`: no `sudo` permission\n- (L2) Non-root user running `xinstall --sudo subcmd -ic`: `sudo` is called when necessary\n- (L3) Non-root user running `sudo xinstall subcmd -ic`: root permission everywhere\n- (L3) root user running `xinstall subcmd -ic`: root permission everywhere\n\nThe suggested way is to run `xinstal --sudo subcmd -ic` using non-root user if `sudo` permission is required.\n`sudo xinstall subcmd -ic` might have side effect as some tools are installed to the local user directory,\nin which case `sudo xinstall subcmd -ic` installs the tool into `/root/` \nwhich might not what you wwant.\n\n## Proxy\n\nSome tools used by xinstall respect environment variables `http_proxy` and `https_proxy`.\nExporting those 2 evironment variable will make most part of xinstall work if proxy is required. \n```\nexport http_proxy=http://server_ip:port\nexport https_proxy=http://server_ip:port\n```\n',
    'author': 'Benjamin Du',
    'author_email': 'longendu@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/legendu-net/xinstall',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
