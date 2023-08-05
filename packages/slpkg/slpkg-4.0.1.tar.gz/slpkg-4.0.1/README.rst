***********
slpkg 4.0.1
***********

Slpkg is a powerful software package manager that installs, updates, and removes packages on
`Slackware <http://www.slackware.com/>`_ based systems. It automatically computes dependencies and
figures out what things should occur to install packages. Slpkg makes it easier to maintain groups
of machines without having to manually update.

Slpkg works in accordance with the standards of the organization `SlackBuilds.org <https://www.slackbuilds.org>`_
to build packages. Also uses the Slackware Linux instructions for installation,
upgrading or removing packages.

What makes slpkg distinguish from the other tools; The user-friendliness it's a primary
target as well as easy to understand and use, also uses colours to highlight packages and
display warning messages, etc.

Look in the `EXAMPLES.md <https://gitlab.com/dslackw/slpkg/blob/master/EXAMPLES.md>`_ file to explore some examples.


Asciicast
---------


.. image:: https://gitlab.com/dslackw/images/raw/master/slpkg/asciicast.png
    :target: https://asciinema.org/a/3uFNAOX8o16AmKKJDIvdezPBa
    :width: 200px


Install
-------

Install from the official third party `SBo repository <https://slackbuilds.org/repository/15.0/system/slpkg/>`_, or directly from the source:


.. code-block:: bash

    $ wget slpkg-4.0.1.tar.gz
    $ tar xvf slpkg-4.0.1.tar.gz
    $ cd slpkg-4.0.1
    $ ./install.sh


Usage
-----

.. code-block:: bash

    $ slpkg update
    $ slpkg -s sbo install <package_name>
    $ slpkg --help


Copyright
---------

Copyright 2014-2022 © Dimitris Zlatanidis. 

Slackware® is a Registered Trademark of Patrick Volkerding. 

Linux is a Registered Trademark of Linus Torvalds.
