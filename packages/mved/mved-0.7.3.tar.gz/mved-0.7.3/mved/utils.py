# This file is part of mved, the bulk file renaming tool.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

"""Utility functions for mved."""

import re

from mved.colors import NO_COLORS


def __make_escape_tables():
    __TBL_ESCAPES = {
        "\\\\": "\\",
        r"\a": "\a",
        r"\b": "\b",
        r"\f": "\f",
        r"\n": "\n",
        r"\r": "\r",
        r"\t": "\t",
        r"\v": "\v"
    }
    esc = {}
    unesc = {}
    for i in range(0, 0x100):
        e = f"\\x{i:02x}"
        if i >= 0x80:
            # replace surrogateescapes with "\xHH"
            c = 0xdc00 | i
            esc[c] = e
            u = chr(c)
        else:
            # replace control chars with "\xHH"
            if i < 0x20 or i == 0x7f:
                esc[i] = e
            u = chr(i)
        unesc[e] = u
    for e, u in __TBL_ESCAPES.items():
        esc[ord(u)] = e
        unesc[e] = u
    return esc, unesc


TBL_ESCAPE, TBL_UNESCAPE = __make_escape_tables()
REGEX_ESCAPE = re.compile(r"\\x[0-9a-fA-F]{2}|\\.")
del __make_escape_tables


def escapepath(arg):
    return arg.translate(TBL_ESCAPE)


def unescapepath(arg):
    if "\\" not in arg:
        # shortcut if no escapes found
        return arg

    def repl(match):
        s = match.group()
        if s.startswith("\\x"):
            s = s.lower()
        return get_unescape(s, None) or s[1:]

    get_unescape = TBL_UNESCAPE.get
    return REGEX_ESCAPE.sub(repl, arg)


def format_files(names, lim_before=3, lim_after=1,
                 separator=", ", colors=NO_COLORS):
    limit = lim_before + lim_after
    parts = []
    omitted = 0
    last = None
    for i, name in enumerate(names, 1):
        if i >= limit:
            last = name
            omitted += 1
        else:
            parts.append(escapepath(name))
    if last is not None:
        omitted -= 1
        if omitted > 0:
            parts.append(f"[{colors.stats}{omitted:+d} files{colors.reset}]")
        parts.append(escapepath(last))
    separator = colors.listsep + separator + colors.reset
    return separator.join(parts)


def is_valid_name(name):
    if not isinstance(name, str):
        raise TypeError
    if '\0' in name:
        return False
    name = name.rstrip('/')
    _, _, name = name.rpartition('/')
    return name not in ('', '.', '..')


class InternalError(Exception):
    pass


# vim:set sw=4 et:
