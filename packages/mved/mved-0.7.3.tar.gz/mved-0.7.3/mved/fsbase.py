# This file is part of mved, the bulk file renaming tool.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

"""Base for file system access."""


class FsBase(object):

    # Pure string operations

    def basename(self, p):
        p = p.rstrip('/')
        return p[(p.rfind('/') + 1):]

    def dirname(self, p):
        p = p.rstrip('/')
        head = p[:(p.rfind('/') + 1)]
        if head:
            return head.rstrip('/') or "/"
        return ""

    def splitpath(self, p):
        slash = p.startswith("/")
        st, _, en = p.rstrip("/").rpartition("/")
        if not st and slash:
            st = "/"
        return st, en

    # Methods accessing the file system

    def realpath(self, path):
        raise NotImplementedError()

    # Methods building upon file system methods

    def makeparent(self, filename, exist_ok=True):
        dn = self.dirname(filename)
        if dn:
            self.makedirs(dn, exist_ok=exist_ok)

    def realdir(self, path):
        if not path:
            raise OSError(f"Invalid argument: {path!r}")
        path = path.rstrip('/')
        if not path:
            return "/"
        dn, bn = self.splitpath(path)
        if bn in ('.', '..'):
            raise OSError(f"Invalid argument: {path!r}")
        if not dn:
            dn = "."
        dn = self.realpath(dn + "/")
        if dn == "/":
            return "/" + bn
        return dn + "/" + bn

    def uniqfiles(self, files):
        seen, num_seen = set(), 0
        res = []
        realdir = self.realdir
        for f in files:
            seen.add(realdir(f))
            if len(seen) > num_seen:
                num_seen += 1
                res.append(f)
        return res


# vim:set sw=4 et:
