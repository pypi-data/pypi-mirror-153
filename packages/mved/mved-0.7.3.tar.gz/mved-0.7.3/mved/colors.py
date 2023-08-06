# This file is part of mved, the bulk file renaming tool.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

"""Output text colorization."""

import weakref
from functools import lru_cache


class Colors(object):

    def __init__(self, colors={}):
        self.__dict__.update(colors)
        self.for_readline = ReadlineColors(self)

    def __getattr__(self, name):
        return ""

    def colorize(self, text, name):
        return f"{getattr(self, name)}{text}{self.reset}"


class ReadlineColors(object):

    def __init__(self, colors):
        self.colors = colors

    def __getattr__(self, name):
        value = getattr(self.colors, name)
        if not value or not isinstance(value, str):
            return value
        return "\001" + value + "\002"


TERMCOLORS = {
    'diffremove': '\033[31m',
    'diffadd': '\033[32m',
    'diffsep': '\033[35m',
    'listsep': '\033[35m',
    'conflict': '\033[31m',
    'fileno': '\033[33m',
    'stats': '\033[36m',
    'action': '\033[33m',
    'action_delete': '\033[31m',
    'revertprompt': '\033[31m',
    'revertchoice': '\033[33m',
    'successprompt': '\033[32m',
    'successchoice': '\033[33m',
    'prompt': '\033[;34m',
    'promptchoice': '\033[1;34m',
    'reset': '\033[m',
}

NO_COLORS = Colors()


@lru_cache(3)
def _colors_for_file(weakfile):
    if weakfile().isatty():
        return Colors(TERMCOLORS)
    else:
        return NO_COLORS


def colors_for_file(file):
    return _colors_for_file(weakref.ref(file))


# vim:set sw=4 et:
