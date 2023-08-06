# This file is part of mved, the bulk file renaming tool.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

"""Access to real file system operations."""

import os
import shutil
import tempfile

from mved.fsbase import FsBase


class RealFs(FsBase):

    def __init__(self):
        # Directly used file system methods
        self.listdir = os.listdir
        self.walk = os.walk
        self.exists = os.path.exists
        self.isdir = os.path.isdir
        self.isfile = os.path.isfile
        self.islink = os.path.islink
        self.makedirs = os.makedirs
        self.symlink = os.symlink
        self.move = shutil.move
        self.rename = os.rename
        self.unlink = os.unlink
        self.rmdir = os.rmdir
        self.realpath = os.path.realpath
        self.readlink = os.readlink

    def copy(self, src, dst):
        return shutil.copy2(src, dst, follow_symlinks=False)

    def move_temp(self, path, suffix=None, prefix=None):
        dir, base = self.splitpath(self.realdir(path))
        fd, name = tempfile.mkstemp(dir=dir, suffix=suffix, prefix=prefix)
        isdir = self.isdir(path)
        if isdir:
            # cannot move directory atomically
            os.unlink(name)
        try:
            self.move(path, name)
        except BaseException as e:
            if not isdir:
                import warnings
                size = os.path.getsize(name)
                if size == 0:
                    self.unlink(name)
                else:
                    warnings.warn(
                        f"move failed but temporary file {name!r} "
                        f"is not empty, not deleting {name!r}.")
                os.close(fd)
            raise e
        else:
            return name


# vim:set sw=4 et:
