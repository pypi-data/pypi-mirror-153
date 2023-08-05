# Slpkg

##### Slpkg Examples

Enable or disable default repositories, edit '`/etc/slpkg/repositories.conf`' file or with the command.
(require pythondialog, install with '`slpkg -s sbo python3-pythondialog`'):

```
$ slpkg repo-enable
```

![alt text](https://gitlab.com/dslackw/images/raw/master/slpkg/repo_enable.png)


If you use slpkg for the first time, you will have to create and update the packages
lists. This command must be executed to update the packages lists:

```
$ slpkg update

Update repository [slack] ... Done
Update repository [sbo] ... Done
Update repository [alien] ... Done
Update repository [slacky] ... Done
Update repository [conrad] ... Done
Update repository [slonly] ... Done
Update repository [ktown] ... Done
Update repository [salix] ... Done
Update repository [slacke] ... Done
Update repository [slackl] ... Done
Update repository [multi] ... Done
Update repository [msb] ... Done

```
Update specifically repositories:

```
$ slpkg update --repositories=sbo,msb,slacky
```

Also you can check ChangeLog.txt for changes, like:

```
$ slpkg -c sbo

+==============================================================================
| Repository         Status
+==============================================================================
  sbo                News in ChangeLog.txt

Summary
===============================================================================
From 1 repositories need 1 updating. Run the command 'slpkg update'.


$ slpkg --check

+==============================================================================
| Repository         Status
+==============================================================================
  slack              No changes in ChangeLog.txt
  sbo                News in ChangeLog.txt
  slacky             News in ChangeLog.txt
  alien              No changes in ChangeLog.txt
  rlw                No changes in ChangeLog.txt

Summary
===============================================================================
From 5 repositories need 2 updating. Run the command 'slpkg update'.
```

Add and remove custom repositories:

```
$ slpkg repo-add ponce http://ponce.cc/slackware/slackware64-14.2/packages/

Repository 'ponce' successfully added

$ slpkg repo-add repo1 file:///home/user1/repos/alien/

Repository 'repo1' successfully added

$ slpkg repo-remove ponce

Repository 'ponce' successfully removed

```

View information about the repositories:

```
$ slpkg repo-list

+==============================================================================
| Repo id  Repo URL                                            Default   Status
+==============================================================================
  alien    http://www.slackware.com/~alien/slackbuilds/        yes     disabled
  ktown    http://alien.slackbook.org/ktown/                   yes     disabled
  msb      http://slackware.org.uk/msb/                        yes      enabled
  multi    http://www.slackware.com/~alien/multilib/           yes     disabled
  ponce    http://ponce.cc/slackware/slackware64-14.2/packa~   no       enabled
  rested   http://taper.alienbase.nl/mirrors/people/alien/r~   yes     disabled
  rlw      http://rlworkman.net/pkgs/                          yes     disabled
  salix    http://download.salixos.org/                        yes     disabled
  sbo      http://slackbuilds.org/slackbuilds/                 yes      enabled
  slack    http://ftp.cc.uoc.gr/mirrors/linux/slackware/       yes      enabled
  slacke   http://ngc891.blogdns.net/pub/                      yes     disabled
  slackl   http://www.slackel.gr/repo/                         yes     disabled
  conrad    http://slack.conraid.net/repository/slackware64-~   yes     disabled
  slacky   http://repository.slacky.eu/                        yes     disabled
  slonly   https://slackonly.com/pub/packages/                 yes     disabled

Repositories summary
===============================================================================
3/14 enabled default repositories and 1 custom.
For enable or disable default repositories edit '/etc/slpkg/repositories.conf'
file.

$ slpkg repo-info alien

Default: yes
Last updated: Tue Dec 23 11:48:31 UTC 2014
Number of packages: 3149
Repo id: alien
Repo url: http://www.slackware.com/~alien/slackbuilds/
Status: enabled
Total compressed packages: 9.3 Gb
Total uncompressed packages: 36.31 Gb
```

Installing packages from the repositories (supporting multi packages):

```
$ slpkg -s sbo brasero
Reading package lists... Done
Resolving dependencies... Done

The following packages will be automatically installed or upgraded
with new version:

+==============================================================================
| Package                 New version        Arch    Build  Repos          Size
+==============================================================================
Installing:
  brasero                 3.12.1             x86_64         SBo
Installing for dependencies:
  orc                     0.4.23             x86_64         SBo
  gstreamer1              1.4.5              x86_64         SBo
  gst1-plugins-base       1.4.5              x86_64         SBo
  gst1-plugins-bad        1.4.5              x86_64         SBo

Installing summary
===============================================================================
Total 5 packages.
5 packages will be installed, 0 already installed and 0 package
will be upgraded.

Would you like to continue [y/N]?
```

Example install multi packages:

```
$ slpkg -s sbo brasero pylint atkmm
Reading package lists... Done
Resolving dependencies... Done

The following packages will be automatically installed or upgraded
with new version:

+==============================================================================
| Package                 New version        Arch    Build  Repos          Size
+==============================================================================
Installing:
  brasero                 3.12.1             x86_64         SBo
  pylint-1.3.1            1.3.1              x86_64         SBo
  atkmm                   2.22.7             x86_64         SBo
Installing for dependencies:
  libsigc++               2.2.11             x86_64         SBo
  glibmm                  2.36.2             x86_64         SBo
  cairomm                 1.10.0             x86_64         SBo
  pangomm                 2.34.0             x86_64         SBo
  six-1.8.0               1.8.0              x86_64         SBo
  pysetuptools-17.0       17.0               x86_64         SBo
  logilab-common-0.63.2   0.63.2             x86_64         SBo
  astroid-1.3.6           1.3.6              x86_64         SBo
  orc                     0.4.23             x86_64         SBo
  gstreamer1              1.4.5              x86_64         SBo
  gst1-plugins-base       1.4.5              x86_64         SBo
  gst1-plugins-bad        1.4.5              x86_64         SBo

Installing summary
===============================================================================
Total 15 packages.
10 packages will be installed, 5 already installed and 0 package
will be upgraded.

Would you like to continue [y/N]?
```

Example from 'alien' repository:

```
$ slpkg -s alien atkmm
Reading package lists... Done
Resolving dependencies... Done

+==============================================================================
| Package                 New version        Arch    Build  Repos          Size
+==============================================================================
Installing:
  atkmm                   2.22.6             x86_64  1      alien         124 K
Installing for dependencies:
  libsigc++               2.2.10             x86_64  2      alien         128 K
  glibmm                  2.32.1             x86_64  1      alien        1012 K
  cairomm                 1.10.0             x86_64  2      alien         124 K
  pangomm                 2.28.4             x86_64  1      alien         124 K

Installing summary
===============================================================================
Total 5 packages.
5 packages will be installed, 0 will be upgraded and 0 will be reinstalled.
Need to get 124 Kb of archives.
After this process, 620 Kb of additional disk space will be used.

Would you like to continue [y/N]?
```

Close auto resolve dependencies:

```
$ slpkg -s alien atkm --resolve-off
Reading package lists... Done

The following packages will be automatically installed or upgraded
with new version:

+==============================================================================
| Package                 New version        Arch    Build  Repos          Size
+==============================================================================
Installing:
  atkmm                   2.22.6             x86_64  1      alien         124 K

Installing summary
===============================================================================
Total 1 package.
1 package will be installed, 0 will be upgraded and 0 will be reinstalled.
Need to get 124 Kb of archives.
After this process, 620 Kb of additional disk space will be used.

Would you like to continue [y/N]?
```

Build packages and passing variables to the script:


First export variable(s) like:

```
$ export FFMPEG_ASS=yes FFMPEG_X264=yes
```

And then run as you know:

```
$ slpkg -s sbo ffmpeg

```

or

```
$ slpkg -n ffmpeg
```

or if already script and source donwloaded:

```
$ slpkg -a ffmpeg.tar.gz ffmpeg-2.1.5.tar.bz2
```

Tracking all the dependencies of packages, and also displays the installed packages:

```
$ slpkg -t sbo brasero
Resolving dependencies... Done

+=========================
| brasero dependencies   :
+=========================
\
 +---[ Tree of dependencies ]
 |
 +--1 orc
 |
 +--2 gstreamer1
 |
 +--3 gst1-plugins-base
 |
 +--4 gst1-plugins-bad
 |
 +--5 libunique
```

Check if the dependencies used:

```
$ slpkg -t sbo Flask --check-deps
Resolving dependencies... Done

+=============================
| Package Flask dependencies :
+=============================
\
 +---[ Tree of dependencies ]
 |
 +--1: pysetuptools is dependence on --> Flask, bpython, pip, pylint
 |
 +--2: MarkupSafe is dependence on --> Flask
 |
 +--3: itsdangerous is dependence on --> Flask
 |
 +--4: Jinja2 is dependence on --> Flask
 |
 +--5: werkzeug is dependence on --> Flask
```

Drawing the dependencies diagram:

```
$ slpkg -t sbo flexget --graph=image.x11
```

![alt text](https://gitlab.com/dslackw/images/raw/master/slpkg/deps2.png)

```
$ slpkg -t sbo Flask --check-deps --graph=image.x11
Resolving dependencies... Done

+=============================
| Package Flask dependencies :
+=============================
\
 +---[ Tree of dependencies ]
 |
 +--1: pysetuptools is dependence on --> APScheduler, Flask, Jinja2, MarkupSafe, astroid, autopep8, blessings, bpython, cffi, cryptography, curtsies, itsdangerous, monty, ndg_httpsclient, pip, pyOpenSSL, pylint, wcwidth
 |
 +--2: MarkupSafe is dependence on --> Flask, Jinja2
 |
 +--3: itsdangerous is dependence on --> Flask
 |
 +--4: Jinja2 is dependence on --> Flask
 |
 +--5: werkzeug is dependence on --> Flask
```

![alt text](https://gitlab.com/dslackw/images/raw/master/slpkg/deps3.png)


Drawing the dependencies ascii diagram:

```
$ slpkg -t sbo botocore --graph=ascii

                                   +---------------------------------+
                                   |                                 |
                                   |                                 |
                                   |    +---------+                  |
                                   |    |         |                  |
                                   |    |         |                  |
                  +----------------+----+----+    |                  |
                  |                |    |    |    |                  |
+--------------+  |  +--------------------+  |  +-----------------+  |
|   jmespath   | -+- |      botocore      |  +- | python-dateutil |  |
+--------------+  |  +--------------------+     +-----------------+  |
  |               |    |           |    |         |                  |
  |               |    |           |    |         |                  |
  |               |    |           |    |         |                  |
+--------------+  |  +----------+  |    |       +-----------------+  |
| pysetuptools | -+  |  bcdoc   | -+----+------ |       six       | -+
+--------------+     +----------+  |    |       +-----------------+
  |                    |           |    |
  |                    |           |    |
  |                    |           |    |
  |                  +----------+  |    |
  |                  | docutils | -+    |
  |                  +----------+       |
  |                                     |
  +-------------------------------------+
```

Print the dependencies status used by packages:

```
$ slpkg deps-status

+==============================================================================
| Dependencies                    Packages
+==============================================================================
  astroid                         pylint
  logilab-common                  pylint
  werkzeug                        Flask
  cryptography                    bpython
  ndg_httpsclient                 bpython
  enum34                          bpython
  pyOpenSSL                       bpython
  curtsies                        bpython
  six                             bpython, pylint
  cffi                            bpython
  python-requests                 bpython
  pysetuptools                    Flask, bpython, pip, pylint
  MarkupSafe                      Flask
  Pygments                        bpython
  Jinja2                          Flask
  pycparser                       bpython
  blessings                       bpython
  greenlet                        bpython
  pyasn1                          bpython

Summary
===============================================================================
Found 19 dependencies in 4 packages.
```

Use the additional option '`--graph=[image]`' to drawing the dependencies diagram:

```
$ slpkg deps-status --graph=image.x11
```

![alt text](https://gitlab.com/dslackw/images/raw/master/slpkg/deps.png)


Check if your packages is up to date or they have changes in ChangeLog.txt:

```
$ slpkg -c sbo

+==============================================================================
| Repository         Status
+==============================================================================
  sbo                News in ChangeLog.txt

Summary
===============================================================================
From 1 repositories need 1 updating. Run the command 'slpkg update'.
```

Check for new versions:

```
$ slpkg -c sbo --upgrade
Checking... Done
Reading package lists... Done
Resolving dependencies... Done

The following packages will be automatically installed or upgraded
with new version:

+==============================================================================
| Package                 New version        Arch    Build  Repos          Size
+==============================================================================
Upgrading:
  astroid-1.3.2           1.3.4              x86_64         SBo
  jdk-7u51                8u31               x86_64         SBo
Installing for dependencies:
  six-1.7.3               1.8.0              x86_64         SBo
  logilab-common-0.60.1   0.63.2             x86_64         SBo
  pysetuptools-6.1        7.0                x86_64         SBo

Installing summary
===============================================================================
Total 5 packages.
0 package will be installed, 2 already installed and 3 packages
will be upgraded.

Would you like to continue [y/N]?


$ slpkg -c slacky --upgrade
Checking... Done
Reading package lists... Done
Resolving dependencies... Done

+==============================================================================
| Package                 New version        Arch    Build  Repos          Size
+==============================================================================
Upgrading:
  gstreamer1-1.4.1        1.4.4              x86_64  1      slacky       1563 K

Installing summary
===============================================================================
Total 1 package.
0 package will be installed, 1 will be upgraded and 0 will be reinstalled.
Need to get 1.53 Mb of archives.
After this process, 14.55 Mb of additional disk space will be used.

Would you like to continue [y/N]?
```

Check if your Slackware distribution is up to date.
This option works independently of the others i.e you don't need before you updating the 
packages lists:

```
$ slpkg -c slack --upgrade
Reading package lists... Done

These packages need upgrading:

+==============================================================================
| Package                   New version      Arch     Build  Repos         Size
+==============================================================================
Upgrading:
  dhcpcd-6.0.5              6.0.5            x86_64   3      Slack         92 K
  samba-4.1.0               4.1.11           x86_64   1      Slack       9928 K
  xscreensaver-5.22         5.29             x86_64   1      Slack       3896 K

Installing summary
===============================================================================
Total 3 package will be upgrading and 0 will be installed.
Need to get 13.58 Mb of archives.
After this process, 76.10 Mb of additional disk space will be used.

Would you like to continue [y/N]?
```

Upgrade only distribution:

```
$ slpkg -c slack --upgrade --skip="multi:*multilib*,ktown:*"  // This upgrade
Checking... Done                                              // distribution
                                                              // and skip all
Slackware64 'stable' v14.2 distribution is up to date         // packages from
                                                              // ktown repository
                                                              // and multilib
                                                              // from multi.
```

Skip packages when upgrading:

```
$ slpkg -c sbo --upgrade --skip=pip,jdk     // Available options:
Checking... Done                            // repository:*string*
Reading package lists... Done               // repository:string*
Resolving dependencies... Done              // repository:*string

The following packages will be automatically installed or upgraded
with new version:

+==============================================================================
| Package                 New version        Arch    Build  Repos          Size
+==============================================================================
Upgrading:
  cffi-1.0.1              1.1.0              x86_64         SBo
Installing for dependencies:
  pysetuptools-17.0       17.0               x86_64         SBo
  pycparser-2.12          2.13               x86_64         SBo

Installing summary
===============================================================================
Total 3 packages.
0 package will be installed, 1 already installed and 2 packages
will be upgraded.

Would you like to continue [y/N]?
```

View slackbuilds.org site in your terminal. Read files, download, build or install:

```
$ slpkg -n bitfighter
Reading package lists... Done

+==============================================================================
|                             SlackBuilds Repository
+==============================================================================
| 14.2 > Games > bitfighter
+===============================================================================
| Package url: http://slackbuilds.org/repository/14.2/games/bitfighter/
+===============================================================================
| Description: multi-player combat game
| SlackBuild: bitfighter.tar.gz
| Sources: bitfighter-019c.tar.gz, classic_level_pack.zip
| Requirements: OpenAL, SDL2, speex, libmodplug
+===============================================================================
| README               View the README file
| SlackBuild           View the .SlackBuild file
| Info                 View the .info file
| Doinst.sh            View the doinst.sh file
| Download             Download this package
| Build                Download and build this package
| Install              Download/Build/Install
| Clear                Clear screen
  Quit                 Quit
+================================================================================
  Choose an option > _
```

Use the dialog utility to help you find the packages:

```
$ slpkg -n --checklist
Reading package lists...
```

![alt text](https://gitlab.com/dslackw/images/raw/master/slpkg/pythondialog5.png)

```
$ slpkg -n perl --checklist
Reading package lists...
```

![alt text](https://gitlab.com/dslackw/images/raw/master/slpkg/pythondialog6.png)


Auto tool to build a package:
Two files termcolor.tar.gz and termcolor-1.1.0.tar.gz must be in the same directory.
(slackbuild script & source code or extra sources if needed)

```
$ slpkg -a termcolor.tar.gz termcolor-1.1.0.tar.gz

termcolor/
termcolor/slack-desc
termcolor/termcolor.info
termcolor/README
termcolor/termcolor.SlackBuild
termcolor-1.1.0/
termcolor-1.1.0/CHANGES.rst
termcolor-1.1.0/COPYING.txt
termcolor-1.1.0/README.rst
termcolor-1.1.0/setup.py
termcolor-1.1.0/termcolor.py
termcolor-1.1.0/PKG-INFO
running install
running build
running build_py
creating build
creating build/lib
copying termcolor.py -> build/lib
running install_lib
creating /tmp/SBo/package-termcolor/usr
creating /tmp/SBo/package-termcolor/usr/lib64
creating /tmp/SBo/package-termcolor/usr/lib64/python2.7
creating /tmp/SBo/package-termcolor/usr/lib64/python2.7/site-packages
copying build/lib/termcolor.py ->
/tmp/SBo/package-termcolor/usr/lib64/python2.7/site-packages
byte-compiling /tmp/SBo/package-termcolor/usr/lib64/python2.7/site-packages/termcolor.py
to termcolor.pyc
running install_egg_info
Writing
/tmp/SBo/package-termcolor/usr/lib64/python2.7/site-packages/termcolor-1.1.0-py2.7.egg-info

Slackware package maker, version 3.14159.

Searching for symbolic links:

No symbolic links were found, so we wont make an installation script.
You can make your own later in ./install/doinst.sh and rebuild the
package if you like.

This next step is optional - you can set the directories in your package
to some sane permissions. If any of the directories in your package have
special permissions, then DO NOT reset them here!

Would you like to reset all directory permissions to 755 (drwxr-xr-x) and
directory ownerships to root.root ([y]es, [n]o)? n

Creating Slackware package:  /tmp/termcolor-1.1.0-x86_64-1_SBo.tgz

./
usr/
usr/lib64/
usr/lib64/python2.7/
usr/lib64/python2.7/site-packages/
usr/lib64/python2.7/site-packages/termcolor.py
usr/lib64/python2.7/site-packages/termcolor.pyc
usr/lib64/python2.7/site-packages/termcolor-1.1.0-py2.7.egg-info
usr/doc/
usr/doc/termcolor-1.1.0/
usr/doc/termcolor-1.1.0/termcolor.SlackBuild
usr/doc/termcolor-1.1.0/README.rst
usr/doc/termcolor-1.1.0/CHANGES.rst
usr/doc/termcolor-1.1.0/PKG-INFO
usr/doc/termcolor-1.1.0/COPYING.txt
install/
install/slack-desc

Slackware package /tmp/termcolor-1.1.0-x86_64-1_SBo.tgz created.

Total build time for package termcolor : 1 Sec
```

Upgrade, install the packages like Slackware command '`upgradepkg --install-new`':

```
$ slpkg -u --install-new /tmp/termcolor-1.1.0-x86_64-1_SBo.tgz

+==============================================================================
| Installing new package ./termcolor-1.1.0-x86_64-1_SBo.tgz
+==============================================================================

Verifying package termcolor-1.1.0-x86_64-1_SBo.tgz.
Installing package termcolor-1.1.0-x86_64-1_SBo.tgz:
PACKAGE DESCRIPTION:
# termcolor (ANSII Color formatting for output in terminal)
#
# termcolor allows you to format your output in terminal.
#
# Project URL: https://pypi.python.org/pypi/termcolor
#
Package termcolor-1.1.0-x86_64-1_SBo.tgz installed.
```

Install mass-packages:

```
$ slpkg -u --install-new *.t?z
```

or

```
$ slpkg -i *.t?z
```

Slpkg auto detect Slackware binary packages (.tgz, .txz, .tlz and .tbz) for installation:

```
$ slpkg pysed-0.7.8-x86_64-1_SBo.tgz

pysed-0.7.8-x86_64-1_SBo.tgz

+==============================================================================
| Choose a Slackware command:
+==============================================================================
| i)  installpkg
| r)  upgradepkg --reinstall
| u)  upgradepkg --install-new
+==============================================================================
 > _
```

Search packages from the enabled repositories:

```
$ slpkg -F aria2

Packages with name matching [ aria2 ]

+==============================================================================
| Repository  Package                                                      Size
+==============================================================================
  sbo         aria2-1.18.10                                                 0 K
  slonly      aria2-1.18.10-x86_64-1_slack.txz                           1124 K
  salix       aria2-1.18.1-x86_64-1rl.txz                                1052 K
  conrad      aria2-1.18.10-x86_64-1cf.txz                               1140 K

Found summary
===============================================================================
Total found 4 packages in 4 repositories.


$ slpkg -F pyqt5 AAA --case-ins

Packages with name matching [ pyqt5, AAA ]

+==============================================================================
| Repository  Package                                                      Size
+==============================================================================
  slack       aaa_base-14.2-x86_64-1.txz                                   12 K
  slack       aaa_elflibs-14.2-x86_64-3.txz                              4316 K
  slack       aaa_terminfo-5.8-x86_64-1.txz                                44 K
  sbo         jaaa-0.8.4                                                    0 K
  sbo         python3-PyQt5-5.5                                             0 K
  slonly      jaaa-0.8.4-x86_64-1_slack.txz                                40 K
  slonly      python3-PyQt5-5.5-x86_64-1_slack.txz                       3088 K

Found summary
===============================================================================
Total found 7 packages in 3 repositories.
```

Find the installed packages:

```
$ slpkg -f apr

Sckages with matching name [ apr ]

[ installed ] [ 1.1M ] - apr-1.5.2-x86_64-1
[ installed ] [ 530K ] - apr-util-1.5.4-x86_64-2
[ installed ] [ 40K ] - xf86dgaproto-2.1-noarch-1
[ installed ] [ 50K ] - xineramaproto-1.2.1-noarch-1

Found summary
===============================================================================
Total found 4 matching packages.
Size of installed packages 1.71 Mb.


$ slpkg -f python --third-party

Packages with matching name [ python ]

[ installed ] [ 1.4M ] - bpython-0.17.1-x86_64-1_SBo
[ installed ] [ 590K ] - python-certifi-2018.11.29-x86_64-1_SBo
[ installed ] [ 1.9M ] - python-chardet-3.0.4-x86_64-1_SBo
[ installed ] [ 220K ] - python-libtmux-0.8.0-x86_64-1_SBo
[ installed ] [ 50K ] - python-notify2-0.3.1-x86_64-1_SBo
[ installed ] [ 1.5M ] - python-requests-2.20.1-x86_64-1_SBo
[ installed ] [ 110K ] - python-scandir-1.8-x86_64-1_SBo
[ installed ] [ 1.5M ] - python-urllib3-1.23-x86_64-1_SBo
[ installed ] [ 440K ] - python2-pythondialog-3.4.0-x86_64-1_SBo
[ installed ] [ 120M ] - python3-3.6.7-x86_64-1_SBo

Found summary
===============================================================================
Total found 10 matching packages.
Size of installed packages 127.68 Mb.
```

Display the contents of the packages:

```
$ slpkg -d termcolor lua

PACKAGE NAME:     termcolor-1.1.0-x86_64-1_SBo
COMPRESSED PACKAGE SIZE:     8.0K
UNCOMPRESSED PACKAGE SIZE:     60K
PACKAGE LOCATION: ./termcolor-1.1.0-x86_64-1_SBo.tgz
PACKAGE DESCRIPTION:
termcolor: termcolor (ANSII Color formatting for output in terminal)
termcolor:
termcolor: termcolor allows you to format your output in terminal.
termcolor:
termcolor:
termcolor: Project URL: https://pypi.python.org/pypi/termcolor
termcolor:
termcolor:
termcolor:
termcolor:
FILE LIST:
./
usr/
usr/lib64/
usr/lib64/python2.7/
usr/lib64/python2.7/site-packages/
usr/lib64/python2.7/site-packages/termcolor.py
usr/lib64/python2.7/site-packages/termcolor.pyc
usr/lib64/python2.7/site-packages/termcolor-1.1.0-py2.7.egg-info
usr/lib64/python3.3/
usr/lib64/python3.3/site-packages/
usr/lib64/python3.3/site-packages/termcolor-1.1.0-py3.3.egg-info
usr/lib64/python3.3/site-packages/__pycache__/
usr/lib64/python3.3/site-packages/__pycache__/termcolor.cpython-33.pyc
usr/lib64/python3.3/site-packages/termcolor.py
usr/doc/
usr/doc/termcolor-1.1.0/
usr/doc/termcolor-1.1.0/termcolor.SlackBuild
usr/doc/termcolor-1.1.0/README.rst
usr/doc/termcolor-1.1.0/CHANGES.rst
usr/doc/termcolor-1.1.0/PKG-INFO
usr/doc/termcolor-1.1.0/COPYING.txt
install/
install/slack-desc

No such package lua: Cant find
```

Removes a previously installed Slackware binary package:

```
$ slpkg -r termcolor

Packages with name matching [ termcolor ]

[ delete ] --> termcolor-1.1.0-x86_64-1_SBo

Removed summary
===============================================================================
Size of removed packages 50.0 Kb.

Are you sure to remove 1 package(s) [y/N]? y

Package: termcolor-1.1.0-x86_64-1_SBo
    Removing...

Removing package /var/log/packages/termcolor-1.1.0-x86_64-1_SBo...
    Removing files:
--> Deleting /usr/doc/termcolor-1.1.0/CHANGES.rst
--> Deleting /usr/doc/termcolor-1.1.0/COPYING.txt
--> Deleting /usr/doc/termcolor-1.1.0/PKG-INFO
--> Deleting /usr/doc/termcolor-1.1.0/README.rst
--> Deleting /usr/doc/termcolor-1.1.0/termcolor.SlackBuild
--> Deleting /usr/lib64/python2.7/site-packages/termcolor-1.1.0-py2.7.egg-info
--> Deleting /usr/lib64/python2.7/site-packages/termcolor.py
--> Deleting /usr/lib64/python2.7/site-packages/termcolor.pyc
--> Deleting /usr/lib64/python3.3/site-packages/__pycache__/termcolor.cpython-33.pyc
--> Deleting /usr/lib64/python3.3/site-packages/termcolor-1.1.0-py3.3.egg-info
--> Deleting /usr/lib64/python3.3/site-packages/termcolor.py
--> Deleting empty directory /usr/lib64/python3.3/site-packages/__pycache__/
WARNING: Unique directory /usr/lib64/python3.3/site-packages/ contains new files
WARNING: Unique directory /usr/lib64/python3.3/ contains new files
--> Deleting empty directory /usr/doc/termcolor-1.1.0/

+==============================================================================
| Package: termcolor-1.1.0 removed
+==============================================================================
```

Remove packages with all dependencies and check if used as dependency:
(Presupposes install with the option '`slpkg -s <repository> <packages>`')

```
$ slpkg -r Flask --check-deps

Packages with name matching [ Flask ]

[ delete ] --> Flask-0.10.1-x86_64-1_SBo

Removed summary
===============================================================================
Size of removed packages 1.2 Mb.

Are you sure to remove 1 package [y/N]? y

+==============================================================================
| Found dependencies for package Flask:
+==============================================================================
| pysetuptools-18.0.1
| MarkupSafe-0.23
| werkzeug-0.9.4
| Jinja2-2.7.3
| itsdangerous-0.24
+==============================================================================
| Size of removed dependencies 5.52 Mb
+==============================================================================

Remove dependencies (maybe used by other packages) [y/N]? y


+==============================================================================
|                              !!! WARNING !!!
+==============================================================================
| pysetuptools is dependency of the package --> Flask
| MarkupSafe is dependency of the package --> Flask
| werkzeug is dependency of the package --> Flask
| Jinja2 is dependency of the package --> Flask
| itsdangerous is dependency of the package --> Flask
| pysetuptools is dependency of the package --> flake8
| pysetuptools is dependency of the package --> pip
| pysetuptools is dependency of the package --> pipstat
| pysetuptools is dependency of the package --> pylint
| pysetuptools is dependency of the package --> wcwidth
+==============================================================================
+==============================================================================
| Insert packages to exception remove:
+==============================================================================
 > pysetuptools

.
.
.
+==============================================================================
| Total 5 packages removed
+==============================================================================
| Package Flask-0.10.1 removed
| Package MarkupSafe-0.23 removed
| Package itsdangerous-0.24 removed
| Package Jinja2-2.7.3 removed
| Package werkzeug-0.9.4 removed
+==============================================================================
```

Remove the packages with by TAG:

```
$ slpkg -r _SBo --tag

Packages with name matching [ _SBo ]

[ delete ] --> Jinja2-2.7.3-x86_64-1_SBo
[ delete ] --> MarkupSafe-0.23-x86_64-1_SBo
[ delete ] --> Pafy-0.3.72-x86_64-1_SBo
[ delete ] --> Pulse-Glass-1.02-x86_64-1_SBo
[ delete ] --> Pygments-1.6-x86_64-2_SBo
[ delete ] --> asciinema-1.1.1-x86_64-1_SBo
[ delete ] --> astroid-1.3.8-x86_64-1_SBo
[ delete ] --> autopep8-1.2-x86_64-1_SBo
[ delete ] --> blessings-1.6-x86_64-1_SBo
[ delete ] --> bpython-0.14.2-x86_64-1_SBo
[ delete ] --> cffi-1.1.2-x86_64-1_SBo
[ delete ] --> cryptography-0.8.2-x86_64-1_SBo
[ delete ] --> curtsies-0.1.19-x86_64-1_SBo
[ delete ] --> enum34-1.0.4-x86_64-1_SBo

Removed summary
===============================================================================
Size of removed packages 24.61 Mb.

Are you sure to remove 14 packages [y/N]?
```

Remove the packages using dialog utility:

```
$ slpkg -r _SBo --tag --checklist
```

![alt text](https://gitlab.com/dslackw/images/raw/master/slpkg/pythondialog.png)

```
$ slpkg -r Flask --check-deps --checklist
```

![alt text](https://gitlab.com/dslackw/images/raw/master/slpkg/pythondialog2.png)

![alt text](https://gitlab.com/dslackw/images/raw/master/slpkg/pythondialog3.png)

![alt text](https://gitlab.com/dslackw/images/raw/master/slpkg/pythondialog4.png)


Remove only the third-party packages:

```
$ slpkg -r python --third-party

Packages with name matching [ python ]

[ delete ] --> bpython-0.17.1-x86_64-1_SBo
[ delete ] --> python-certifi-2018.11.29-x86_64-1_SBo
[ delete ] --> python-chardet-3.0.4-x86_64-1_SBo
[ delete ] --> python-libtmux-0.8.0-x86_64-1_SBo
[ delete ] --> python-notify2-0.3.1-x86_64-1_SBo
[ delete ] --> python-requests-2.20.1-x86_64-1_SBo
[ delete ] --> python-scandir-1.8-x86_64-1_SBo
[ delete ] --> python-urllib3-1.23-x86_64-1_SBo
[ delete ] --> python2-pythondialog-3.4.0-x86_64-1_SBo
[ delete ] --> python3-3.6.7-x86_64-1_SBo

Removed summary
===============================================================================
Size of removed packages 127.68 Mb.


+==============================================================================
|                            *** WARNING ***
| Before you use third-party option, be sure you have updated the package
| lists. Run the command 'slpkg update' and 'slpkg -c slack --upgrade'
+==============================================================================

Are you sure to remove 10 packages [y/N]?
```

Build and install the packages that have added to the queue:

```
$ slpkg -q roxterm SDL2 CEGUI --add

Add packages in queue:

roxterm
SDL2
CEGUI


$ slpkg -q roxterm --remove (or '`slpkg -q --remove`' remove all packages)

Remove packages from queue:

roxterm


$ slpkg -q list

Packages in queue:

SDL2
CEGUI


$ slpkg -q build (build only packages from queue)

$ slpkg -q install (install packages from queue)

$ slpkg -q build-install (build and install)
```

Add or remove packages in blacklist file manually from the '`/etc/slpkg/blacklist`' file or with the following options:

```
$ slpkg -b live555 speex faac --add

Add packages in blacklist:

live555
speex
faac


$ slpkg -b speex --remove (or 'slpkg -b --remove' remove all packages)

Remove packages from blacklist:

speex


$ slpkg -b list

Packages in blacklist:

live555
faac


```

Print a package description:

```
$ slpkg -p alien vlc --color=green

vlc (multimedia player for various audio and video formats)

VLC media player is a highly portable multimedia player for various
audio and video formats (MPEG-1, MPEG-2, MPEG-4, DivX, mp3, ogg, ...)
as well as DVDs, VCDs, and various streaming protocols.
It can also be used as a server to stream in unicast or multicast in
IPv4 or IPv6 on a high-bandwidth network.


vlc home: http://www.videolan.org/vlc/
```

Man page it is available for full support:

```
$ man slpkg
```


##### Python modules


Slpkg has been designed it to work as cli tool however you can use some modules in your
own python code.

Get the package dependencies from the sbo repository:

```
>>> from slpkg.sbo.dependency import Requires
>>> Requires(flag="").sbo("vlc")
[['libass', 'libdc1394', 'libdvbpsi', 'libmpeg2', 'libupnp', 'lua', 'portaudio',
'twolame', 'opus', 'ffmpeg', 'libwebp', 'gsm', 'opencv', 'libtar', 'libkate', '
faac', 'libdca', 'libmatroska', 'libshout', 'speex', 'avahi', 'projectM', 'jack-
audio-connection-kit', 'libsidplay2', 'zvbi', 'faad2', 'libavc1394', 'libmodplug
', 'musepack-tools', 'vcdimager', 'dirac', 'gnome-vfs', 'live555', 'qt5', 'rtmpd
ump', 'libdvdcss', 'fluidsynth', 'schroedinger', 'libminizip', 'chromaprint', 'x
264', 'x265', 'libbluray'], ['libmp4v2'], ['libebml'], ['libdaemon'], ['ftgl'],
['libcuefile', 'libreplaygain'], ['gnome-mime-data', 'libbonobo'], ['ORBit2'], [
'libxkbcommon', 'libinput'], ['libwacom']]
```

Example from binary repository:

```
>>> from slpkg.binary.dependency import Dependencies
>>> Dependencies(repo="slonly", black="").binary(name="Flask", flag="")
[['Jinja2', 'click', 'itsdangerous', 'werkzeug'], ['MarkupSafe']]
```

Grab packages from the sbo repository:

```
>>> from slpkg.sbo.greps import SBoGrep
>>> SBoGrep(name="").names()
...
```

Grab the package sources links:

```
>>> SBoGrep(name="jdk").source()
'http://download.oracle.com/otn-pub/java/jdk/8u152-b16/aa0333dd3019491ca4f6ddbe7
8cdb6d0/jdk-8u152-linux-x64.tar.gz'
```

Grap a package requires:

```
>>> SBoGrep(name="Flask").requires()
['werkzeug', 'Jinja2', 'itsdangerous', 'click']
```

Grap a package checksum:

```
>>> SBoGrep(name="Flask").checksum()
['97278dfdafda98ba7902e890b0289177']
```

Grap a package description:

```
>>> SBoGrep(name="Flask").description()
'Flask (Microframework for Python)'
```

Grap the package files:

```
>>> SBoGrep(name="Flask").files()
'Flask.SlackBuild Flask.info README slack-desc'
```

Grab the packages for binary repository:

```
>>> from slpkg.binary.greps import repo_data
>>> from slpkg.binary.repo_init import RepoInit
>>> PACKAGES_TXT, mirror = RepoInit("slonly").fetch()
>>> name, location, size, unsize = repo_data(PACKAGES_TXT, repo="slonly", flag="")
```

Find a package url from the sbo repository:

```
from slpkg.sbo.search import sbo_search_pkg
>>> sbo_search_pkg(name="Flask")
'http://slackbuilds.org/slackbuilds/14.2/python/Flask/'
```

Check if the package exist in the binary repository:

```
>>> from slpkg.binary.search import search_pkg
>>> search_pkg(name="vlc", repo="alien")
'vlc'
```

Read files from the sbo repository:

```
>>> from slpkg.sbo.search import sbo_search_pkg
>>> from slpkg.sbo.read import ReadSBo
>>> url = sbo_search_pkg(name="libreoffice")
>>> ReadSBo(url).readme("README")
'LibreOffice is a productivity suite that is compatible with other major\noffice
 suites, and available on a variety of platforms. It is free\nsoftware and there
fore free to download, use and distribute.\n\nThis script builds a Slackware pac
kage from the official binary (RPM\'s)\ndistributed by The Document Foundation.
 Everything needed by the\napplication should be built statically into it, so th
ere aren\'t any\ndependencies not satisfied by a normal installation.\n\nBe sure
 to look at the script for some optional things you can do when\nbuilding.\n\nNO
TE: See the separate SlackBuild script for the language packs.\n\nNOTE2: To keep
 LibreOffice installed concurrently with OpenOffice, run the\n       included "o
pen-libre-together.sh" script saved in the documentation\n       directory of th
is package to patch the .desktop menu files.\n\nNOTE3: LibreOffice versions chan
ge quite often. If the version for which\n       this script was written is no l
onger available, look for it at:\n       http://download.documentfoundation.org/
libreoffice/old/stable/\n       It will go there after the next release.\n
 You can also try building the newer version using:\n       # VERSION="x.y.z" ./
libreoffice.SlackBuild\n       This *might* work, but upstream has a habit of ch
anging the naming\n       and structure of the files, etc. between versions, so:
 YMMV.\n'

>>> ReadSBo(url).slackbuild("libreoffice", ".SlackBuild")
...

>>> ReadSBo(url).info("libreoffice", ".info")
'PRGNAM="libreoffice"\nVERSION="5.4.3"\nHOMEPAGE="http://www.libreoffice.org"\nD
OWNLOAD="http://download.documentfoundation.org/libreoffice/stable/5.4.3/rpm/x86
/LibreOffice_5.4.3_Linux_x86_rpm.tar.gz"\nMD5SUM="bada10945a979537ff42268462fc8b
de"\nDOWNLOAD_x86_64="http://download.documentfoundation.org/libreoffice/stable/
5.4.3/rpm/x86_64/LibreOffice_5.4.3_Linux_x86-64_rpm.tar.gz"\nMD5SUM_x86_64="4b0b
46a6d2df74a1446837ba76af07fd"\nREQUIRES="jdk"\nMAINTAINER="Willy Sudiarto Raharj
o"\nEMAIL="willysr@slackbuilds.org"\n'


>>> ReadSBo(url).doinst("doinst.sh")
'if [ -x /usr/bin/update-desktop-database ]; then\n  /usr/bin/update-desktop-dat
abase -q usr/share/applications\nfi\n\nif [ -x /usr/bin/update-mime-database ];
then\n  /usr/bin/update-mime-database usr/share/mime >/dev/null 2>&1\nfi\n\nif [
-x /usr/bin/gtk-update-icon-cache ]; then\n  for theme in gnome locolor hicolor
; do\n    if [ -e usr/share/icons/$theme/icon-theme.cache ]; then\n      /usr/b
in/gtk-update-icon-cache -f usr/share/icons/$theme >/dev/null 2>&1\n    fi\n  do
ne\nfi\'
```

Get the Slackware version:

```
>>> from slpkg.slack.slack_version import slack_ver
>>> slack_ver()
'14.2'
```

Find a Slackware package:

```
>>> from slpkg.pkg.find import find_package
>>> find_package(find_pkg="vlc", directory="/var/log/packages/")
['vlc-2.2.6-x86_64-1alien']
```

Check for the installed packages:

```
>>> from slpkg.pkg.installed import GetFromInstalled
>>> GetFromInstalled(package="ffmpeg").name()
'ffmpeg'
>>> GetFromInstalled(package="ffmpeg").version()
'3.2.4'
```

##### Copyright

- Copyright 2014-2018 © Dimitris Zlatanidis
- Slackware® is a Registered Trademark of Patrick Volkerding.
- Linux is a Registered Trademark of Linus Torvalds.
