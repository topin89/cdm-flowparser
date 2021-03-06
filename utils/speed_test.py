#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# codimension - graphics python two-way code editor and analyzer
# Copyright (C) 2010-2017  Sergey Satskiy <sergey.satskiy@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Speed test for the Codimension control flow parser"""

import os, os.path, sys
import datetime
import cdmcfparser
from cdmcfparser import getControlFlowFromFile, VERSION


def collectFiles(path, files):
    """Collects python files"""
    if not path.endswith(os.path.sep):
        path += os.path.sep
    for item in os.listdir(path):
        if os.path.isdir(path + item):
            collectFiles(path + item, files)
        if os.path.isfile(path + item) and item.endswith(".py"):
            if item.startswith("__"):
                continue
            files.append(os.path.abspath(path + item))
            continue


def getTotalSize(files):
    """Provides the total files size"""
    total = 0
    for item in files:
        total += os.path.getsize(item)
    return total


def cdmcfparserTest(files):
    """Loop for the codimension parser"""
    count = 0
    for item in files:
        # print("Processing " + item + " ...")
        tempObj = getControlFlowFromFile(item)
        count += 1
    print("cdmcf: processed " + str(count) + " file(s)")


print("Speed test measures the time required for "
      "cdmcfparser to parse python files.")
print("Parser version: " + VERSION)
print("Module location: " + cdmcfparser.__file__)


pythonFiles = []
if len(sys.argv) > 1:
    # File names are expected
    for fname in sys.argv[1:]:
        if not os.path.exists(fname):
            print("Cannot find file specified: '" + fname + "'")
            sys.exit(1)
        pythonFiles.append(os.path.abspath(fname))
    print("Files to test: " + str(len(pythonFiles)))
else:
    print("Collecting a list of python files...")
    paths = list(sys.path)
    if '' in paths:
        paths.remove('')
    for path in paths:
        if os.path.isdir(path):
            collectFiles(path, pythonFiles)
    pythonFiles = set(pythonFiles)
    print("Collected " + str(len(pythonFiles)))
    print("Total file size: " + str(getTotalSize(pythonFiles)))


# timing for cdmcfparser
start = datetime.datetime.now()
cdmcfparserTest(pythonFiles)
end = datetime.datetime.now()

print("cdmcf timing:")
print("Start: " + str(start))
print("End:   " + str(end))
print("Delta: " + str(end - start))
