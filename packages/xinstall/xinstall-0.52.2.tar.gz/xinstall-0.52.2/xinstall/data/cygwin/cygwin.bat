@echo off
C:
chdir C:\cygwin\bin
set EDITOR=vim
set VISUAL=vim
set CYGWIN=codepage:oem tty binmode title
rxvt -sr -sl 10000 -fg white -bg black -fn fixedsys -fb fixedsys -tn cygwin -e bash --login -i
