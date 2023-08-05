#!/usr/bin/python3
# -*- coding: utf-8 -*-

# models.py file is part of slpkg.

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


from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Text

from slpkg.__metadata__ import MetaData as _meta_

lib_path = _meta_.lib_path
db = _meta_.db

DATABASE_URI = f"sqlite:///{lib_path}{db}"
engine = create_engine(DATABASE_URI)

session = sessionmaker(engine)()
Base = declarative_base()


class SBoTable(Base):

    __tablename__ = "sbotable"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    location = Column(Text)
    files = Column(Text)
    version = Column(Text)
    download = Column(Text)
    download64 = Column(Text)
    md5sum = Column(Text)
    md5sum64 = Column(Text)
    requires = Column(Text)
    short_description = Column(Text)


Base.metadata.create_all(engine)
