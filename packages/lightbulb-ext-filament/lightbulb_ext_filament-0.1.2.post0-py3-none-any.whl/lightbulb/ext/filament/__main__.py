# -*- coding: utf-8 -*-
# Copyright © tandemdude 2020-present
#
# This file is part of Filament.
#
# Filament is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Filament is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Filament. If not, see <https://www.gnu.org/licenses/>.
import argparse
import importlib
import sys

from . import __version__

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--new", action="store_true", help="Create a template project in the current directory.")
parser.add_argument(
    "-s",
    "--style",
    default="lightbulb",
    choices=["lightbulb", "filament"],
    help="The command style to use in the created project. Defaults to 'lightbulb'",
)

args = parser.parse_args()
if args.new:
    if args.style not in ["lightbulb", "filament"]:
        sys.stderr.write("Invalid value provided for '--style'. Must be one of: 'lightbulb', 'filament'")
        sys.exit()

    from . import _t

    _t.run(args)

    sys.exit()


sys.stderr.write(f"lightbulb-filament ({__version__})\n")
importlib.import_module("lightbulb.__main__")
