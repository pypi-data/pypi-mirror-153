# [xinstall](https://github.com/legendu-net/xinstall): Easy Cross-platform Installation and Configuration of Apps

## Install xinstall

    :::bash
    pip3 install -U xinstall

## Usage

1. Run `xinstall -h` for the help doc.
        
2. Below is an example of install SpaceVim and configure it.

        xinstall svim -ic
    
3. In case `xinstall` is not on the search path, 
    you can use `python3 -m xinstall.main` instead. 
    For example, 
    to check the help doc.
    
        python3 -m xinstall.main -h
        
### sudo Permission

xinstall has 3 levels of `sudo` permission.

- (L1) Non-root user running `xinstall subcmd -ic`: no `sudo` permission
- (L2) Non-root user running `xinstall --sudo subcmd -ic`: `sudo` is called when necessary
- (L3) Non-root user running `sudo xinstall subcmd -ic`: root permission everywhere
- (L3) root user running `xinstall subcmd -ic`: root permission everywhere

The suggested way is to run `xinstal --sudo subcmd -ic` using non-root user if `sudo` permission is required.
`sudo xinstall subcmd -ic` might have side effect as some tools are installed to the local user directory,
in which case `sudo xinstall subcmd -ic` installs the tool into `/root/` 
which might not what you wwant.

## Proxy

Some tools used by xinstall respect environment variables `http_proxy` and `https_proxy`.
Exporting those 2 evironment variable will make most part of xinstall work if proxy is required. 
```
export http_proxy=http://server_ip:port
export https_proxy=http://server_ip:port
```
