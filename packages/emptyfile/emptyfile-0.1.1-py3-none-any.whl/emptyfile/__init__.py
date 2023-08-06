#! /usr/bin/python3
# -*- coding: utf-8 -*-

#############################################################################
#
#    Copyright [yyyy] [name of copyright owner]
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#############################################################################
"""
Constructor module for the package and cli logic.
"""

import argparse
import os
import sys

from emptyfile.remover import Remover


def execute(args: list = None) -> argparse.Namespace:
    """
    Command line arguments options and logic.

    Parameters
    ----------
    args : list, optional
        contrived command line arguments, by default None

    Returns
    -------
    argparse.Namespace
        the command line options indicated by user.
    """
    if not args:
        if not sys.argv[1:]:
            args = ["-h"]
        else:
            args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        "emptyfile",
        description="empty file remover",
    )

    parser.add_argument(
        "path",
        help="base directory and starting point.",
        nargs="*",
        action="store",
    )

    parser.add_argument(
        "-d",
        "--dir",
        help="remove empty directories instead of empty files.",
        dest="folders",
        action="store_true",
    )

    parser.add_argument(
        "--exclude-names",
        help="one or more file/directory names that will be ignored while "
        "searching for items to remove.",
        nargs="+",
        dest="ex_names",
        default=[],
    )

    parser.add_argument(
        "--exclude-ext",
        help="one or more file extensions to be ignored during "
        "file/directory analysis.",
        nargs="+",
        dest="ex_ext",
        default=[],
    )
    exists = os.path.exists
    isdir = os.path.isdir

    ns = nspace = parser.parse_args(args)
    if not ns.path:
        extfilt = [x for x in ns.ex_ext if exists(x) and isdir(x)]
        if len(extfilt) > 0:
            ns.path = extfilt
            ns.ex_ext = ns.ex_ext[: -len(extfilt)]
        else:
            ns.path = [x for x in ns.ex_names if exists(x) and isdir(x)]
            ns.ex_names = ns.ex_names[: -len(ns.path)]
    Remover(nspace)
    return nspace
