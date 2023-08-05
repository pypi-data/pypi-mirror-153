#!/usr/bin/python3
# -*- coding: utf-8 -*-

# messages.py file is part of slpkg.

# Copyright 2014-2022 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Slpkg is a user-friendly package manager for Slackware installations

# https://gitlab.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import itertools

from slpkg.__metadata__ import MetaData as _meta_


class Msg:
    """Messages control
    """
    def __init__(self):
        self.meta = _meta_
        self.green = _meta_.color["GREEN"]
        self.grey = _meta_.color["GREY"]
        self.red = _meta_.color["RED"]
        self.cyan = _meta_.color["CYAN"]
        self.endc = _meta_.color["ENDC"]

    def pkg_not_found(self, bol, pkg, message, eol):
        print(f"{bol}No such package {pkg}: {message}{eol}")

    def pkg_found(self, prgnam):
        print(f"| Package {prgnam} is already installed")

    def pkg_installed(self, pkg):
        print(f"| Package {pkg} installed")

    def build_FAILED(self, prgnam):
        self.template(78)
        print(f"| Some error on the package {prgnam} "
              f"[ {self.red}FAILED{self.endc} ]")
        self.template(78)
        print(f"| See the log file in '{self.cyan}"
              f"/var/log/slpkg/sbo/build_logs{self.endc}' "
              f"directory or read the README file")
        self.template(78)
        print()   # new line at end

    def template(self, max_len):
        print("+" + "=" * max_len)

    def checking(self):
        print(f"{self.grey}Checking...{self.endc}  ", end="", flush=True)

    def reading(self):
        print(f"{self.grey}Reading package lists...{self.endc}  ",
              end="", flush=True)

    def resolving(self):
        print(f"{self.grey}Resolving dependencies...{self.endc}  ",
              end="", flush=True)

    def done(self):
        print(f"\b{self.green}Done{self.endc}\n", end="")

    def pkg(self, count):
        message = "package"
        if count > 1:
            message = message + "s"

        return message

    def not_found(self, if_upgrade):
        if if_upgrade:
            print("\nNot found packages for upgrade\n")

        else:
            print("\nNot found packages for installation\n")

    def upg_inst(self, if_upgrade):
        if not if_upgrade:
            print("Installing:")

        else:
            print("Upgrading:")

    def answer(self):
        if self.meta.default_answer in ["y", "Y"]:
            answer = self.meta.default_answer

        else:
            try:
                answer = input("Would you like to continue [y/N]? ")
            except EOFError:
                raise SystemExit("\n")
        return answer

    def security_pkg(self, pkg):
        print()
        self.template(78)
        print(f"| {' ' * 27}{self.red}*** WARNING ***{self.endc}")
        self.template(78)
        print(f"| Before proceed with the package '{pkg}' will you must read\n"
              f"| the README file. You can use the command "
              f"'slpkg -n {pkg}'")
        self.template(78)
        print()

    def reference(self, install, upgrade):
        self.template(78)
        print(f"| Total {len(install)} {self.pkg(len(install))} installed and "
              f"{len(upgrade)} {self.pkg(len(upgrade))} upgraded")
        self.template(78)

        for installed, upgraded in itertools.zip_longest(install, upgrade):

            if upgraded:
                print(f"| Package {upgraded} upgraded successfully")

            if installed:
                print(f"| Package {installed} installed successfully")

        self.template(78)
        print()

    def matching(self, packages):
        print(f"\nNot found package with the name "
              f"[ {self.cyan}{''.join(packages)}{self.endc} ]. "
              "Matching packages:\nNOTE: Not dependencies are resolved\n")
