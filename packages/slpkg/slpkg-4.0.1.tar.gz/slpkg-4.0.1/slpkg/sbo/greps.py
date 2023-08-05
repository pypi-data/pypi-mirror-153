#!/usr/bin/python3
# -*- coding: utf-8 -*-

# greps.py file is part of slpkg.

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


from slpkg.utils import Utils
from slpkg.__metadata__ import MetaData as _meta_
from slpkg.models.models import SBoTable, session


class SBoGrep(Utils):
    """Grabs data from sbo database
    """
    def __init__(self, name):
        self.name = name
        self.meta = _meta_
        self.db = self.meta.db
        self.arch64 = "x86_64"
        self.session = session

    def _names_grabbing(self):
        """Generator that collecting all packages names
        """
        names = self.session.query(SBoTable.name).all()
        for n in names:
            yield n[0]

    def names(self):
        """Alias method convert generator and return
        a list
        """
        return list(self._names_grabbing())

    def source(self):
        """Grabs sources downloads links
        """
        source, source64 = self.session.query(
            SBoTable.download, SBoTable.download64).filter(
                SBoTable.name == self.name).first()

        return self._sorting_arch(source, source64)

    def requires(self):
        """Grabs package requirements
        """
        requires = self.session.query(
            SBoTable.requires).filter(
                SBoTable.name == self.name).first()

        return requires[0].split()

    def version(self):
        """Grabs package version
        """
        version = self.session.query(
            SBoTable.version).filter(
                SBoTable.name == self.name).first()

        return version[0]

    def checksum(self):
        """Grabs checksum string
        """
        md5sum, md5sum64, = [], []
        mds5, md5s64 = self.session.query(
            SBoTable.md5sum, SBoTable.md5sum64).filter(
                SBoTable.name == self.name).first()

        if mds5:
            md5sum.append(mds5)
        if md5s64:
            md5sum64.append(md5s64)

        return self._sorting_arch(md5sum, md5sum64)

    def description(self):
        """Grabs package description
        """
        desc = self.session.query(
            SBoTable.short_description).filter(
                SBoTable.name == self.name).first()

        return desc[0]

    def files(self):
        """Grabs files
        """
        files = self.session.query(
            SBoTable.files).filter(
                SBoTable.name == self.name).first()

        return files[0]

    def _sorting_arch(self, arch, arch64):
        """Returns sources by arch
        """
        if self.meta.arch == self.arch64 and arch64:
            return arch64

        return arch
