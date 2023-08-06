# This file is part of mved, the bulk file renaming tool.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

"""File reference helpers."""

from mved.utils import escapepath
from mved.colors import NO_COLORS


class SrcFile(object):

    def __init__(self, i, src, dests=None):
        self.index = i
        self.src = src
        self.dests = [src] if dests is None else dests

    def __repr__(self):
        return f"SrcFile({self.index + 1} {self.src})"

    def reset(self):
        self.dests = [self.src]

    def is_modified(self, fs=None):
        dests = self.dests
        if len(dests) != 1:
            return True
        if dests[0] != self.src:
            return fs is None or fs.realdir(dests[0]) != fs.realdir(self.src)
        return False

    def get_diff(self, numbers=False, colors=NO_COLORS):
        try:
            from simplediff import diff
        except ImportError:
            return f"{self.src} -> {self.dests}"
        else:
            parts = []
            c_res = colors.reset
            c_fileno = colors.fileno
            if numbers:
                parts.append(
                    f"{c_fileno}[{c_res}{self.index + 1}{c_fileno}]{c_res} ")
            src = escapepath(self.src)
            dests = self.dests
            if not dests:
                # when removing file show as deleted text
                dests = ('',)
            for i, dest in enumerate(dests):
                if i > 0:
                    parts.append(colors.diffsep + " + ")
                for ty, text in diff(src, escapepath(dest)):
                    if ty == '+':
                        color = colors.diffadd
                    elif ty == '-':
                        color = colors.diffremove
                    elif ty == '=':
                        color = colors.reset
                    parts.append(color + text)
            parts.append(colors.reset)
            return ''.join(parts)


class DestRef(object):

    def __init__(self, file, dest):
        self.file = file
        self.dest = dest

    def __repr__(self):
        return f"DestRef({self.file} {self.dest})"


# vim:set sw=4 et:
