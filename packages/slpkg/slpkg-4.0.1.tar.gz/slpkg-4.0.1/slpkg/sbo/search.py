#!/usr/bin/python3
# -*- coding: utf-8 -*-

# search.py file is part of slpkg.

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


from slpkg.repositories import Repo
from slpkg.slack.slack_version import slack_ver
from slpkg.models.models import SBoTable, session


def sbo_search_pkg(name):
    """Search for package path in SLACKBUILDS.TXT file and
    return url
    """
    location = session.query(SBoTable.location).filter(
        SBoTable.name == name).first()

    repo = Repo()
    sbo = repo.default_repository()["sbo"]
    sbo_url = f"{sbo}{slack_ver()}/"

    return f"{sbo_url}{location[0][2:]}/"
