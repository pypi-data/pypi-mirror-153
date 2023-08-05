## This file was created to explain some peculiarities of repositories used by the slpkg.


*NOTE: For more informations, refer directly to the repositories*


## Default repositories:

For the -current users who they use the sbo repository:
 SlackBuilds.org (sbo) FAQ(15):
 Slackware current is not supported, but as a general rule, the scripts
 should work on it as well.

Rworkman's (rlw) repository use dependencies where displayed in a central site
 '`http://rlworkman.net/pkgs/`' and only those. Unfortunately there is no fixed reference
 dependencies in the file PACKAGES.TXT. You can make changes in '`/etc/slpkg/rlworkman.deps`'
 file.

Conraid's (conrad) repository must be used only from Slackware64 current users and it has no
 reference dependencies.

Slackel.gr (slackl) repository must be used only from Slackware{x86, x86_64} -current users.

MSB (msb) repository has one ChangeLog.txt file for three sub-repositories {1.14, 1.16, latest}.
 So if you have updated the list of packages with the version 1.14 and you want to switch to
 version 1.16 you must run '`slpkg upgrade`' instead of '`slpkg update`'. MSB (msb) repository
 has no reference to the dependencies. Similarly apply and for the repository Cinnamon (csb)
 but with the different versions. Both repositories Mate and Cinnamon support Slackware -current
 x86_64 but not x86.

Slonly repository don't support -current for x86 arch.

Alien's ktown (ktown), Alien's multilib (multi), Slacke E17 and E18, slack-n-free, csb,
 mles and Alien's restricted repository has no reference dependencies.

IMPORTANT: For Alien's (Eric Hameleers) repositories (alien, multi and ktown) should run
 '`slpkg upgrade`' instant '`slpkg update`', if you want to spend from -stable in -current or
  not, because there is no different file '`ChangeLog.txt`' for each version.


## Custom repositories:

There is the possibility of adding the repository directly from the user enough to address
 the '`PACKAGES.TXT`' files and '`CHECKSUMS.md5`' at least. If not is there file '`ChangeLog.txt`'
 will get warning messages that the '`ChangeLog.txt`' file can not be read but not worry, the process
 is completed normally have each time you run the command '`slpkg update`' the package lists for such
 a repository will be recreated from start automatically.

Sometimes you may experience some problems with these repositories such as the not correctly
 resolve dependencies, and this may happen some specificities separate list which unfortunately
 can not be calculated, good is the report these problems.


## Slackware ARM repositories:

Slackware ARM users will must use only two repositories at the moment slack and sbo.
