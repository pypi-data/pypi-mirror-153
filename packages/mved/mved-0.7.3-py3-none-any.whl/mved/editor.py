# This file is part of mved, the bulk file renaming tool.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

"""Text and stream editor handling."""

import logging
import os
import shlex
import subprocess
from tempfile import TemporaryFile, NamedTemporaryFile

from mved.files import SrcFile
from mved.utils import escapepath, unescapepath

log = logging.getLogger(__name__)


class Editor(object):

    def __init__(self, files):
        self.files = files

    def _write_file(self, out, reset, sources=True):
        numwidth = len(str(len(self.files)))
        num_fmt = f"{{:0>{numwidth}d}} ".format

        def write_path(number, path, *, is_source=False):
            res = num_fmt(number) + escapepath(path) + '\n'
            if is_source:
                res = "# " + res
            out.write(res)

        if self.files and not reset:
            for i, entry in enumerate(self.files, 1):
                if sources and entry.is_modified():
                    write_path(i, entry.src, is_source=True)
                for dest in entry.dests:
                    write_path(i, dest)
        else:
            for i, entry in enumerate(self.files, 1):
                write_path(i, entry.src)

    def _read_file(self, tempfile):
        files = [SrcFile(i, f.src, dests=[])
                 for i, f in enumerate(self.files)]
        for i, line in enumerate(tempfile, 1):
            line = line.lstrip().rstrip("\n")
            if not line or line.startswith("#"):
                continue
            number, _sep, path = line.partition(" ")
            path = unescapepath(path)
            if path:
                try:
                    index = int(number)
                    files[index - 1].dests.append(path)
                except IndexError:
                    log.warning("invalid index in line %d: %d", i, index)
                except ValueError:
                    log.warning("invalid line: %d: %s", i, escapepath(line))
        return files

    def _edit(self, filename, program=None):
        program = (program
                   or os.environ.get('VISUAL', None)
                   or os.environ.get('EDITOR', "vi"))
        arg = shlex.quote(filename)
        cmd = f"{program} {arg}"
        log.debug("executing editor %r", cmd)
        return subprocess.call(cmd, shell=True)

    def _stream(self, _file, program):
        log.debug("executing stream editor %r", program)
        return subprocess.Popen(program, shell=True, text=True,
                                stdin=_file, stdout=subprocess.PIPE)

    def run_editor(self, reset=False, sources=True,
                   program=None, stream=False, do_log=True):
        if program is None and stream:
            raise ValueError("program is requred if stream=True")
        if stream:
            tempfile = TemporaryFile("w+")
        else:
            tempfile = NamedTemporaryFile("w+", suffix=".mved")
        with tempfile:
            self._write_file(tempfile, reset=reset, sources=sources)
            tempfile.flush()
            if stream:
                tempfile.seek(0)
                towith = proc = self._stream(tempfile, program)
                readfile = proc.stdout
            else:
                if self._edit(tempfile.name, program) != 0:
                    if do_log:
                        log.warning("Editor failed; aborting.")
                    return False
                # open the file again in case the editor
                # recreated the file (like `sed -i`)
                towith = readfile = open(tempfile.name, "r")
            with towith:
                files = self._read_file(readfile)
                if stream and proc.wait(1000) != 0:
                    if do_log:
                        log.warning("Editor failed; aborting.")
                    return False
                if reset and all(not f.is_modified() for f in files):
                    # no dests changed, abort reset
                    return True
                self.files = files
                return True

# vim:set sw=4 et:
