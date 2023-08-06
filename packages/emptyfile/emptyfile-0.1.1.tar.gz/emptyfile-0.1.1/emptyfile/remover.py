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
Module containing the core functionality for the emptyfile program.
"""

import os
import shutil
from argparse import Namespace
from pathlib import Path


class Remover:
    """
    Primary class for program, performing all documented functionality.

    Methods
    -------
    __init__ : constructor
    remove_empty_dirs : folder removal algorithm
    remove_empty_files : file removal algorithm
    remove : actual item removal
    """

    def __init__(self, args: Namespace):
        """
        Construct the the Remover class.

        Acts as an entrypoint to the Removal process.

        Parameters
        ----------
        args : Namespace
            argpase.Namespace object containing cli args.
        """
        self.ex_ext = args.ex_ext if args.ex_ext else []
        self.ex_names = args.ex_names if args.ex_names else []
        self.removed = []
        self.paths: list = args.path
        for path in self.paths:
            path = Path(path)
            if args.folders:
                self.remove_empty_dirs(path)
            else:
                self.remove_empty_files(path)

    def remove_empty_dirs(self, path: os.PathLike) -> list:
        """
        Traverse folder recusively looking for empty folders.

        Parameters
        ----------
        path : os.PathLike
            path to root folder

        Returns
        -------
        list
            list of folders removed
        """
        if os.path.isfile(path):
            return self.removed
        if os.path.isdir(path):
            if os.path.basename(path) in self.ex_names:
                print(f"Ignoring {str(path)}...")
                return self.removed
            try:
                contents = os.listdir(path)
            except PermissionError:  # pragma: nocover
                print(f"Access denied: {str(path)}")
                return self.removed
            if len(contents) == 0:
                self.remove(path)
                self.removed.append(str(path))
                print(f"# {len(self.removed)}: {str(path)}")
                return self.removed
            for subpath in contents:
                full = os.path.join(path, subpath)
                self.remove_empty_dirs(full)
        return self.removed

    @staticmethod
    def remove(path: os.PathLike):
        """
        Delete files and folders in an unrecoverable way.

        Parameters
        ----------
        path : os.PathLike
            path to file or folder that needs removing
        """
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    def remove_empty_files(self, path: os.PathLike) -> list:
        """
        Traverse directory in search for empty 0 length files.

        Parameters
        ----------
        path : os.PathLike
            path to root directory

        Returns
        -------
        list
            list of removed files.
        """
        if path.is_file():
            name, ext = path.name, path.suffix.lower()
            if name not in self.ex_names and ext not in self.ex_ext:
                size = os.path.getsize(path)
                if size == 0:
                    self.removed.append(str(path))
                    self.remove(path)
                    print(f"# {len(self.removed)}: {str(path)}")
                    return self.removed
            else:
                print(f"Ignoring {str(path)}...")
        elif path.is_dir():
            try:
                for item in path.iterdir():
                    self.remove_empty_files(item)
            except PermissionError:  # pragma: nocover
                print(f"Access denied: {str(path)}")
        return self.removed
