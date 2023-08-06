# This file is part of mved, the bulk file renaming tool.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

"""Caching for file system access."""

from functools import lru_cache


class FsCache(object):

    def __init__(self, fs):
        self.fs = fs
        self.known_dirs = set()

    def __getattr__(self, name):
        return getattr(self.fs, name)

    def fscache_clear(self):
        self.known_dirs.clear()
        self.realpath.cache_clear()

    @lru_cache(None)
    def realpath(self, path):
        self.fs.realpath(path)

    def makedirs(self, filename, exist_ok=True):
        known = self.known_dirs
        if filename not in known:
            self.fs.makedirs(filename, exist_ok=exist_ok)
            known.add(filename)
        elif not exist_ok:
            raise OSError(17, f"File exists: {filename!r}")


# vim:set sw=4 et:
