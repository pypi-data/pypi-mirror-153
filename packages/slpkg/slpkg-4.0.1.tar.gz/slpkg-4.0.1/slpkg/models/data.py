#!/usr/bin/python3
# -*- coding: utf-8 -*-

# data.py file is part of slpkg.

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


from progress.bar import Bar
from slpkg.__metadata__ import MetaData as _meta_
from slpkg.models.models import SBoTable, session


class Database:

    def __init__(self):
        self.lib_path = _meta_.lib_path
        self.session = session

    def insert_sbo_table(self):
        """Grabbing data line by line and inserting them into the database
        """

        sbo_tags = [
            "SLACKBUILD NAME:",
            "SLACKBUILD LOCATION:",
            "SLACKBUILD FILES:",
            "SLACKBUILD VERSION:",
            "SLACKBUILD DOWNLOAD:",
            "SLACKBUILD DOWNLOAD_x86_64:",
            "SLACKBUILD MD5SUM:",
            "SLACKBUILD MD5SUM_x86_64:",
            "SLACKBUILD REQUIRES:",
            "SLACKBUILD SHORT DESCRIPTION:"
        ]

        sbo_file = self.open_file(f"{self.lib_path}sbo_repo/SLACKBUILDS.TXT")

        bar = Bar("Creating sbo database", max=len(sbo_file),
                  suffix="%(percent)d%% - %(eta)ds")

        cache = []  # init cache

        for i, line in enumerate(sbo_file, 1):

            for s in sbo_tags:
                if line.startswith(s):
                    line = line.replace(s, "").strip()
                    cache.append(line)

            if (i % 11) == 0:
                data = SBoTable(name=cache[0], location=cache[1],
                                files=cache[2], version=cache[3],
                                download=cache[4], download64=cache[5],
                                md5sum=cache[6], md5sum64=cache[7],
                                requires=cache[8], short_description=cache[9])
                self.session.add(data)

                cache = []  # reset cache after 11 lines

            bar.next()
        bar.finish()

        self.session.commit()

    def open_file(self, file):
        with open(file, "r", encoding="utf-8") as f:
            return f.readlines()
