### Installation


##### Python & OS Support

Slpkg works with Python versions 3.7+ .

Slpkg works on Slackware distribution and possibly in some Slackware based
distribution like SalixOS, Slackel etc.


##### Install slpkg

There are mainly 2 ways:

1. Suggested method, download latest slpkg version from:
   '`https://gitlab.com/dslackw/slpkg/releases`'
   Untar or unzip the archive, change directory in '`slpkg-<version>`'
   and run '`./install.sh`'.
   slpkg auto-installed as Slackware package (root privileges are required).

2. Download binary package from '`https://sourceforge.net/projects/slpkg/files/binary/`'
   and use Slackware command '`upgradepkg --install-new <slpkg binary>`'