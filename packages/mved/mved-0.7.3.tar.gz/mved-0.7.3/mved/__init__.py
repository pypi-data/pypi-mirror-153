# This file is part of mved, the bulk file renaming tool.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

"""Manage files using a text editor.

Run ``mved --help`` for usage.
"""

import argparse
from contextlib import contextmanager
import logging
import sys

from mved.files import SrcFile, DestRef
from mved.utils import (escapepath, format_files, is_valid_name,
                        InternalError)
from mved.editor import Editor
from mved.colors import colors_for_file, NO_COLORS
import mved._version

__version__ = mved._version.__version__

log = logging.getLogger(__name__)


class Change(object):

    applied = False

    # change needing freed src of this change
    child = None

    # list of applied parent changes, for debug output only
    circle_checked = False

    def __init__(self, src):
        self.src = src
        # changes freeing dests of this change
        self.parents = set()

    def __repr__(self):
        clsname = type(self).__name__
        parents = [escapepath(p.src) for p in self.parents]
        child = self.child and self.child.src
        return (f"{clsname}({self.src} -> {self.dests} "
                f"parents:{parents!r} child:{child})")

    def _inconsistent_parents_error(self):
        diff = self.parents.difference(self.done_parents)
        return InternalError(
                f"Inconsistent parents/children:\n"
                f"  self:{self!r}\n  parents:{self.parents!r}\n"
                f"  done:{self.done_parents!r}\n  diff:{diff!r}")

    def ready(self, change):
        self.done_parents.add(change)
        remain = len(self.parents) - len(self.done_parents)
        if remain == 0:
            if self.parents != self.done_parents:
                raise self._inconsistent_parents_error()
            return True
        elif remain > 0:
            return False
        else:
            raise self._inconsistent_parents_error()

    def src_str(self):
        path = self.src
        if isinstance(path, TempLocation):
            return repr(path)
        return escapepath(path)

    def src_path(self):
        path = self.src
        if isinstance(path, TempLocation):
            path = path.tempname
        return path

    def calculate(self, fs):
        raise NotImplementedError()

    def get_message(self, colors=NO_COLORS):
        raise NotImplementedError()

    def apply(self, context):
        raise NotImplementedError()


class TempLocation(object):

    _last_serial = 0

    @classmethod
    def _next_serial(cls):
        cls._last_serial += 1
        return cls._last_serial

    def __init__(self):
        self.serial = TempLocation._next_serial()

    def __repr__(self):
        try:
            tempstr = ": " + escapepath(self.tempname)
        except AttributeError:
            tempstr = ""
        return f"<TempLocation {self.serial}{tempstr}>"


class MoveChange(Change):

    def __init__(self, src, dests):
        Change.__init__(self, src)
        self.dests = dests
        self.applied_dests = set()

    def calculate(self, fs):
        src = self.src
        dests = self.dests
        self.real_dests = real_dests = [fs.realdir(d) for d in dests]

        if not isinstance(src, TempLocation):
            # src is a TempLocation, can only move
            self.real_src = real_src = fs.realdir(src)
        else:
            real_src = None

        if not dests:
            self.op = 'delete'
        elif real_src is None or real_src not in real_dests:
            self.op = 'move'
        else:
            self.op = 'copy'

    def filtered_dests(self, real):
        try:
            real_src = self.real_src
        except AttributeError:
            # src is TempLocation
            real_src = None
        applied_dests = self.applied_dests
        for i, (d, rd) in enumerate(zip(self.dests, self.real_dests)):
            if rd != real_src and d not in applied_dests:
                if real:
                    yield rd
                else:
                    yield d

    def get_message(self, colors=NO_COLORS):
        op = self.op
        c_res = colors.reset
        srcstr = self.src_str()
        if op == 'delete':
            return f"{colors.action}delete{c_res} {srcstr}"
        else:
            sep = colors.listsep + " + " + colors.reset
            deststr = sep.join(map(escapepath, self.filtered_dests(False)))
            return (f"{colors.action}{op}{c_res} "
                    f"{srcstr} {colors.listsep}to{c_res} {deststr}")

    def reset(self):
        self.applied_dests = set()
        self.applied = False

    def apply(self, context):
        op = self.op
        src = self.src_path()
        if op == 'delete':
            context.delete(src)
        else:
            dests = list(self.filtered_dests(True))
            if op == 'move':
                last = dests.pop(-1)
            for dest in dests:
                context.fs.makeparent(dest)
                context.fs.copy(src, dest)
                context.add_revert(MoveChange(dest, ()))
                self.applied_dests.add(dest)
            if op == 'move':
                context.fs.makeparent(last)
                context.fs.move(src, last)
                context.add_revert(MoveChange(last, (src,)))
                self.applied_dests.add(last)
        self.applied = True


class TempMoveChange(Change):

    def __init__(self, src, temploc):
        Change.__init__(self, src)
        if not isinstance(temploc, TempLocation):
            raise TypeError("TempMoveChange needs TempLocation reference")
        self.temploc = temploc

    def calculate(self, fs):
        pass

    def get_message(self, colors=NO_COLORS):
        c_res = colors.reset
        srcstr = self.src_str()
        deststr = repr(self.temploc)
        return (f"{colors.action}rename{c_res} "
                f"{srcstr} {colors.listsep}to{c_res} {deststr}")

    def reset(self):
        self.applied = False

    def apply(self, context):
        src = self.src_path()
        dir, name = context.fs.splitpath(src)
        suffix = "." + name
        tempname = context.fs.move_temp(src, prefix=".mved_temp_",
                                        suffix=suffix)
        self.temploc.tempname = tempname
        context.add_revert(MoveChange(tempname, (src,)))
        self.applied = True


class ChangeError(object):

    def __str__(self):
        return self.get_message()

    def get_message(self, short=True, colors=NO_COLORS):
        return repr(self)


class DestConflict(ChangeError):

    def __init__(self, dest, destrefs):
        self.dest = dest
        self.destrefs = destrefs

    def get_message(self, short=True, colors=NO_COLORS):
        c_res = colors.reset
        deststr = escapepath(self.dest)
        if short:
            files = format_files((ref.file.src for ref in self.destrefs),
                                 colors=colors)
            return (f"{colors.conflict}destination conflict:{c_res} "
                    f"{files} {colors.listsep}->{c_res} {deststr}")
        else:
            c_fileno = colors.fileno
            files = "\n  ".join(
                    f"{c_fileno}[{c_res}{ref.file.index + 1}{c_fileno}]"
                    f"{c_res} {escapepath(ref.file.src)}"
                    for ref in self.destrefs)
            return (f"{colors.conflict}destination conflict:{c_res}\n"
                    f"  {colors.listsep}->{c_res} {deststr}\n"
                    f"  {files}")


class DirConflict(ChangeError):

    def __init__(self, files, is_source, file, dest=None):
        self.file = file
        self.dest = dest
        if not is_source:
            destdict = {}
            for destref in files:
                fdests = destdict.get(destref.file, None)
                if fdests:
                    fdests.append(destref.dest)
                else:
                    destdict[destref.file] = [destref.dest]
            self.destdict = destdict
            files = [ref.file for ref in files]
        self.files = files
        self.is_source = is_source
        self.type = "source" if is_source else "destination"

    def get_message(self, short=True, colors=NO_COLORS):
        c_res = colors.reset
        c_sep = colors.listsep
        if self.dest is not None:
            dirtype = "destination"
            filestr = escapepath(self.dest)
        else:
            dirtype = "source"
            filestr = escapepath(self.file.src)
        if short:
            liststr = format_files((f.src for f in self.files), colors=colors)
        else:
            c_fileno = colors.fileno
            num = self.file.index + 1
            filestr = (f"\n  {c_fileno}[{c_res}{num}{c_fileno}]"
                       f"{c_res} {filestr}")
            if self.is_source:
                liststr = "\n  " + "\n  ".join(
                    f"{c_fileno}[{c_res}{f.index + 1}{c_fileno}]"
                    f"{c_res} {escapepath(f.src)}"
                    for f in self.files)
            else:
                def format_dests(file, dests):
                    src = escapepath(file.src)
                    return (f"{c_fileno}[{c_res}{file.index + 1}{c_fileno}]"
                            f"{c_res} {src} {c_sep}->{c_res} "
                            + format_files(dests, colors=colors))
                liststr = "\n  " + "\n  ".join(
                    format_dests(file, dests)
                    for file, dests in self.destdict.items())
        return (
            f"{colors.conflict}dirctory conflict:{c_res} {c_sep}{dirtype} of "
            f"{c_res}{filestr} {c_sep}is {self.type} of{c_res} {liststr}"
        )


class FileExistsConflict(ChangeError):

    def __init__(self, destref):
        self.destref = destref
        self.path_to_add = destref.dest

    def get_message(self, short=True, colors=NO_COLORS):
        deststr = escapepath(self.destref.dest)
        return f"{colors.conflict}file exists:{colors.reset} {deststr}"


class FileNondirExistsConflict(ChangeError):

    def __init__(self, path, destrefs):
        self.path = path
        self.destrefs = destrefs
        self.path_to_add = path

    def get_message(self, short=True, colors=NO_COLORS):
        c_res = colors.reset
        pathstr = escapepath(self.path)
        files = (ref.file.src for ref in self.destrefs)
        deststr = format_files(files, colors=colors)
        return (f"{colors.conflict}path exists:{c_res} "
                f"{pathstr} {colors.listsep}for{c_res} {deststr}")


class DirError(ChangeError):

    def __init__(self, file, isdelete):
        self.file = file
        if isdelete:
            self.action = "delete"
        else:
            self.action = "copy"

    def get_message(self, short=True, colors=NO_COLORS):
        srcstr = escapepath(self.file.src)
        return (f"{colors.conflict}cannot {self.action} "
                f"directory:{colors.reset} {srcstr}")


class InvalidFilenameError(ChangeError):

    def __init__(self, name, index):
        self.name = name
        self.index = index

    def get_message(self, short=True, colors=NO_COLORS):
        num = self.index + 1
        namestr = escapepath(self.name)
        return (f"{colors.conflict}invalid filename:{colors.reset} "
                f"[{num}] {namestr}")


class MvEdStats(object):

    def __init__(self):
        self.reset()

    def reset(self, files=True, calculated=True):
        if files:
            self.files = 0
        if calculated:
            self.conflicts = 0
            self.copies = 0
            self.moves = 0
            self.deletes = 0
            self.temp_moves = 0

    def get_message(self, colors=NO_COLORS):
        def cformat(count, one, many, color=colors.stats):
            color_reset = ""
            if color:
                color_reset = colors.reset
            if count == 0:
                # never colorize "no"
                color = ""
                color_reset = ""
                count = "no"
                s = many
            elif count == 1:
                s = one
            else:
                s = many
            return color + str(count) + color_reset + " " + s
        msg = [cformat(self.files, "file", "files")]
        changes = self.moves + self.deletes
        msg.append(cformat(changes, "change", "changes"))
        if self.copies:
            msg.append(cformat(self.copies, "copy", "copies"))
        if self.moves:
            msg.append(cformat(self.moves, "move", "moves"))
        if self.temp_moves:
            msg.append(cformat(self.temp_moves, "temp-move", "temp-moves"))
        if self.deletes:
            msg.append(cformat(self.deletes, "deletion", "deletions"))
        if self.conflicts:
            msg.append(cformat(self.conflicts, "conflict", "conflicts",
                               color=colors.conflict))
        return ", ".join(msg)

    @property
    def change_count(self):
        return self.copies + self.moves + self.deletes

    def __str__(self):
        return self.get_message()


class SourceFilenameError(Exception):
    """An added filename is invalid according to `is_valid_name`"""


class FileSet(object):

    def __init__(self, fs):
        self.fs = fs
        self.files = []

    def handle_error(self, e):
        raise e

    def _add_file(self, filename):
        self.files.append(filename)

    def _add_directory(self, dirname, levels=0):
        dirname = dirname.rstrip('/') + '/'
        try:
            flist = self.fs.listdir(dirname)
        except PermissionError as e:
            self.handle_error(e)
        else:
            self.add_files((dirname + f for f in sorted(flist)), levels - 1,
                           all_exist=True)

    def add_files(self, files, levels, all_exist=False):
        for filename in files:
            if not filename or (levels <= 0 and not is_valid_name(filename)):
                raise SourceFilenameError(escapepath(filename))
            islink = self.fs.islink(filename)
            isdir = self.fs.isdir(filename) and not islink
            if not all_exist and not islink and not self.fs.exists(filename):
                self.handle_error(FileNotFoundError(
                    f"No such file or directory: {escapepath(filename)}"))
                continue
            if isdir and levels > 0:
                self._add_directory(filename, levels=levels)
            else:
                if isdir and not filename.endswith("/"):
                    filename += "/"
                self._add_file(filename)

    def add_files_raw(self, files):
        self.files.extend(files)

    def remove_duplicates(self):
        self.files = self.fs.uniqfiles(self.files)

    def srcfiles(self):
        return [SrcFile(i, f) for i, f in enumerate(self.files)]


class ChangeSet(object):

    def __init__(self, files, fs):
        self.srcs = {}
        self.dests = {}
        self.fs = fs
        self.files = files
        self.stats = MvEdStats()
        self.stats.files = len(files)

    def calculate_changes(self):
        self.stats.reset(files=False)
        self.conflicts = []
        self.exist_conflicts = []
        if self._verify_dest_names():
            self._create_changes()
            self._check_dest_conflicts()
            self._check_src_dest_conflicts()
            self._create_dir_maps()
            self._check_exist_nondir_conflicts()
            self._check_dir_conflicts()
            self._check_circles()
        self.stats.conflicts = len(self.conflicts)

    def _verify_dest_names(self):
        """Verifies that all dest filenames are valid.

        Uses mvedutils.is_valid_name() to validate names.

        Returns whether all names are valid.
        """
        valid = True
        for i, file in enumerate(self.files):
            for dest in file.dests:
                if not is_valid_name(dest):
                    self.conflicts.append(InvalidFilenameError(dest, i))
                    valid = False
        return valid

    def _create_changes(self):
        """Create the all_changes map.

        Adds DirConflict for attempts to copy or delete directories.
        """
        fs = self.fs
        self.all_changes = all_changes = {}
        self.changes = changes = set()
        for i, file in enumerate(self.files):
            if file.is_modified(fs):
                change = MoveChange(file.src, file.dests)
                change.calculate(fs)
                changes.add(change)
                all_changes[file] = change
                if not file.dests:
                    self.stats.deletes += 1
                    num_dests = 0
                else:
                    num_dests = len(change.dests)
                    self.stats.copies += num_dests - 1
                    if change.op == 'move':
                        self.stats.moves += 1
                if num_dests != 1 and fs.isdir(file.src):
                    self.conflicts.append(DirError(file, num_dests == 0))

    def _check_dest_conflicts(self):
        """Build the srcs and dests maps and find dest conflicts.

        Creates DestConflict for unresolvable conflicts.

        Can result in circular changes that are checked and
        resolved by _check_circles().
        """
        realdir = self.fs.realdir
        srcs = self.srcs
        dests = self.dests
        for file in self.files:
            rsrc = realdir(file.src)
            exist_src = srcs.get(rsrc, None)
            if exist_src is not None:
                raise InternalError(
                    f"Duplicate src file: {exist_src}, {file}")
            srcs[rsrc] = file
            for dest in file.dests:
                if dest == file.src:
                    rdest = rsrc
                else:
                    rdest = realdir(dest)
                destinfo = dests.get(rdest, None)
                if destinfo is not None:
                    if isinstance(destinfo, DestConflict):
                        destinfo.destrefs.append(DestRef(file, dest))
                    else:
                        # found destination conflict
                        destinfo = DestConflict(
                                rdest, [destinfo, DestRef(file, dest)])
                        dests[rdest] = destinfo
                        self.conflicts.append(destinfo)
                else:
                    dests[rdest] = DestRef(file, dest)

    def _check_src_dest_conflicts(self):
        """Checks for changes that move files to added src files.

        Reparents changes to ensure they are applied in the right order.

        Creates FileExistsConflict of non-added existing dest files.
        """
        for rdest, destinfo in self.dests.items():
            if isinstance(destinfo, DestRef):
                sfile = self.srcs.get(rdest, None)
                if sfile is not None:
                    if sfile != destinfo.file:
                        # found dest in src of other change
                        # resolve by applying src file change first
                        change_src = self.all_changes[sfile]
                        change_dest = self.all_changes[destinfo.file]
                        if change_src.child is not None:
                            raise InternalError('multiple children')
                        change_dest.parents.add(change_src)
                        change_src.child = change_dest
                elif self.fs.isfile(rdest):
                    c = FileExistsConflict(destinfo)
                    self.exist_conflicts.append(c)
                    self.conflicts.append(c)

    def _check_circles(self):
        """Find circular changes created by _check_dest_conflicts.

        Resolves circles with _resolve_circle.
        """
        circles = []

        # A change can only be in at most one circle: more
        # circles would require multiple files to have the same
        # destination, which would result in a DestConflict.

        def mark_checked(c):
            c.circle_checked = True
            c = c.child
            while c and not c.circle_checked:
                c.circle_checked = True
                c = c.child

        def check_circle(c):
            child1 = c
            child2 = c
            while child2 and not child2.circle_checked:
                child2 = child2.child
                if not child2:
                    break
                child2 = child2.child
                child1 = child1.child
                if child1 is child2:
                    circles.append(child1)
                    break

        for c in self.changes:
            check_circle(c)
            mark_checked(c)
        for c in circles:
            self._resolve_circle(c)
            self.stats.temp_moves += 1

    def _resolve_circle(self, change):
        """Resolves a circular change.

        Creates TempMoveChange without parents to move the
        file to a temporary location.

        Creates MoveChange as last child to apply the original
        changes of change.child with the temporary location as src.

        Replaces change.child with these changes.
        """
        child = change.child
        changes = self.changes
        src = child.src
        dests = child.dests

        srcd, srcb = self.fs.splitpath(src)
        temp = TempLocation()

        # Replace 'child' to break up the circle:
        # - 'inital' moves from src to temp
        #   set as parent of 'child.child'
        # - 'final' moves from temp to dest
        #   set as 'change.child'
        #
        # before: change -> child -> child.child
        # after:  change -> final    initial -> child.child
        initial = TempMoveChange(src, temp)
        final = MoveChange(temp, dests)

        initial.child = child.child
        change.child = final

        fparents = set(child.parents)
        final.parents = fparents
        for parent in fparents:
            parent.child = final

        child.child.parents.remove(child)
        child.child.parents.add(initial)

        changes.remove(child)
        changes.add(initial)
        changes.add(final)

        initial.calculate(self.fs)
        final.calculate(self.fs)

    def _create_dir_maps(self):
        """Create the src_dirs and dest_dirs maps.

        Used by _check_exist_nondir_conflicts() and _check_dir_conflicts().
        """
        self.src_dirs = src_dirs = {}
        self.dest_dirs = dest_dirs = {}

        def add_dirs(dirs, path, obj):
            while True:
                path, sep, tail = path.rpartition('/')
                if not path:
                    break
                dirinfo = dirs.get(path, None)
                if dirinfo is not None:
                    dirinfo.append(obj)
                else:
                    dirs[path] = [obj]

        for rsrc, file in self.srcs.items():
            add_dirs(src_dirs, rsrc, file)

        for rdest, destinfo in self.dests.items():
            if isinstance(destinfo, DestRef):
                add_dirs(dest_dirs, rdest, destinfo)

    def _check_exist_nondir_conflicts(self):
        """Detects that files are moved into directories that already
        exist as non-directory.

        If the file is not added, a FileNondirExistsConflict is created.

        If the file is added, a DestConflict is added.
        """
        src_dirs = self.src_dirs
        dest_dirs = self.dest_dirs
        fs = self.fs
        for rpath, destrefs in dest_dirs.items():
            if rpath not in src_dirs:
                src = self.srcs.get(rpath, None)
                if src is None:
                    if not fs.isdir(rpath) and fs.exists(rpath):
                        conflict = FileNondirExistsConflict(rpath, destrefs)
                        self.exist_conflicts.append(conflict)
                        self.conflicts.append(conflict)
                else:
                    # not needed if in changes,
                    # _check_dir_conflicts does it better
                    if src not in self.all_changes:
                        if not fs.isdir(rpath):
                            self.conflicts.append(
                                DestConflict(rpath, destrefs))

    def _check_dir_conflicts(self):
        """Detects that parent directories of files are moved.

        Creates DirConflict if a directory is moved that is used
        by any other added file.
        """
        src_dirs = self.src_dirs
        dest_dirs = self.dest_dirs

        def check_dir(rpath, file, dest=None):
            srcfiles = src_dirs.get(rpath, None)
            if srcfiles is not None:
                self.conflicts.append(
                        DirConflict(srcfiles, True, file, dest=dest))
            destrefs = dest_dirs.get(rpath, None)
            if destrefs is not None:
                self.conflicts.append(
                        DirConflict(destrefs, False, file, dest=dest))

        for file, change in self.all_changes.items():
            check_dir(change.real_src, file)
            for i, (dest, rdest) in enumerate(
                    zip(change.dests, change.real_dests)):
                check_dir(rdest, file, dest=dest)


class Deleter(object):

    def __init__(self):
        self.files = []

    def add(self, fs, path):
        tempname = fs.move_temp(path, prefix='.mved_delete_')
        self.files.append(tempname)
        return tempname

    def finalize(self, fs):
        for f in self.files:
            if fs.isdir(f):
                fs.rmdir(f)
            else:
                fs.unlink(f)


class Reverter(object):

    def __init__(self):
        self.changes = []

    def add(self, change):
        self.changes.append(change)

    def revert(self, fs):
        for change in self.changes:
            change.apply(fs)

    def get_changes(self):
        return list(reversed(self.changes))

    def num_changes(self):
        return len(self.changes)


class ApplyContext(object):

    apply_context = None
    successful = False
    delete_on_success = True
    deleted = False

    def __init__(self, fs, changes, parent=None):
        self.fs = fs
        self.changes = changes
        self.parent = parent
        self.reverter = Reverter()
        self.deleter = Deleter()
        self.autodelete_dirs = False
        self.error = None

    def apply(self, out=sys.stdout, dryrun=False, colors=NO_COLORS):
        parent = self.parent
        if not out:
            colors = NO_COLORS
        error = None
        try:
            for change in self.changes:
                if parent:
                    # always calculate during revert
                    change.calculate(self.fs)
                if out:
                    print(change.get_message(colors=colors), file=out)
                if not dryrun and not change.applied:
                    change.apply(self)
            if self.autodelete_dirs:
                if dryrun:
                    if out:
                        print("delete empty dirs", file=out)
                else:
                    self._delete_empty_dirs(out)
        except BaseException:
            error = sys.exc_info()
        finally:
            self.error = error
            if not dryrun:
                if error is None:
                    self.mark_successful()
                self.finish()

    def _delete_empty_dirs(self, out):
        dirs, num_dirs = set(), 0
        dirname = self.fs.dirname
        for change in self.changes:
            dn = dirname(change.src_path())
            dirs.add(dn)
            if len(dirs) > num_dirs:
                num_dirs = len(dirs)
                try:
                    self.fs.rmdir(dn)
                except OSError:
                    pass
                else:
                    if out:
                        print(f"deleted directory {dn}", file=out)

    def mark_successful(self):
        if self.parent:
            self.parent.reset_changes()
        if self.delete_on_success:
            self.deleter.finalize(self.fs)
            self.deleted = True
        self.successful = True

    def delete_now(self):
        if self.successful and not self.deleted:
            self.deleter.finalize(self.fs)

    def finish(self):
        self.finished = True
        self.add_revert = None
        self.delete = None

    def add_revert(self, change):
        self.reverter.add(change)

    def delete(self, path):
        name = self.deleter.add(self.fs, path)
        self.add_revert(MoveChange(name, (path,)))

    def reset_changes(self):
        for change in self.changes:
            change.reset()

    def create_revert_context(self):
        return ApplyContext(self.fs, self.reverter.get_changes(), self)

    @property
    def num_revert_changes(self):
        return self.reverter.num_changes()

    def get_stats_message(self, colors=NO_COLORS):
        return (f"{colors.stats}{self.num_revert_changes}"
                f"{colors.reset} revertable")


class MvEd(object):

    def __init__(self, fs):
        if fs is None:
            from mved.virtualfs import VirtualFs
            fs = VirtualFs()
        self.fs = fs

        self.sourceset = FileSet(fs)
        self.sourceset.handle_error = self.handle_error

        self.files = []

        self.stats = MvEdStats()
        self.calculated = False
        self.autodelete_dirs = True
        self.have_error = False

        self.apply_context = None

    def handle_error(self, e):
        self.have_error = True
        log.error("%s", e)

    def add_files(self, *files, levels=0):
        self.sourceset.add_files(files, levels)

    def add_files_raw(self, files):
        self.sourceset.add_files_raw(files)

    def apply_sourceset(self):
        self.sourceset.remove_duplicates()
        self.files = self.sourceset.srcfiles()

    def start_editor(self, reset=False, sources=True,
                     program=None, stream=False):
        editor = Editor(self.files)
        if editor.run_editor(reset=reset, sources=sources,
                             program=program, stream=stream):
            self.files = editor.files
            self.calculated = False
            return True
        return False

    def reset(self):
        for f in self.files:
            f.reset()
        del self.changeset
        self.calculated = False
        self.stats.reset(files=False)

    def calculate_changes(self):
        try:
            self.fs.fscache_clear()
        except AttributeError:
            pass
        changeset = ChangeSet(self.files, self.fs)
        changeset.calculate_changes()
        self.stats = changeset.stats
        self.changeset = changeset
        self.calculated = True

    def _iter_work_changes(self):
        for change in self.changeset.changes:
            change.done_parents = set()
        for change in self.changeset.changes:
            if not change.parents:
                while True:
                    yield change
                    child = change.child
                    if not child or not child.ready(change):
                        break
                    change = child

    def create_applier(self):
        if not self.calculated:
            raise Exception("Changes not calculated.")
        context = ApplyContext(self.fs,
                               self._iter_work_changes())
        context._num_changes = len(self.changeset.changes)
        context.autodelete_dirs = self.autodelete_dirs
        return context

    def write_conflicts(self, out, short=True, colors=NO_COLORS):
        for conflict in self.changeset.conflicts:
            out.write(conflict.get_message(short=short, colors=colors) + "\n")

    def write_diff(self, out, numbers=False, colors=NO_COLORS):
        if not self.calculated:
            raise Exception("Changes not calculated.")
        for file in self.files:
            if file.is_modified(self.fs):
                out.write(file.get_diff(numbers=numbers, colors=colors))
                out.write("\n")

    @property
    def has_conflicts(self):
        return bool(self.changeset.conflicts)

    @property
    def conflicts(self):
        return self.changeset.conflicts

    @property
    def has_exist_conflicts(self):
        return bool(self.changeset.exist_conflicts)

    def add_exist_conflict_files(self):
        for conflict in self.changeset.exist_conflicts:
            self.files.append(SrcFile(len(self.files), conflict.path_to_add))
        self.calculated = False


@contextmanager
def setup_terminal():
    from termios import tcgetattr, tcsetattr, TCSADRAIN, ECHO, ICANON
    import tty
    fd = 2
    orig_attrs = tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        attrs = tcgetattr(fd)
        attrs[3] |= ECHO
        attrs[3] &= ~ICANON
        tcsetattr(fd, TCSADRAIN, attrs)
        yield
    finally:
        tcsetattr(fd, TCSADRAIN, orig_attrs)


def make_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version',
                        version=f'%(prog)s {__version__}',
                        help=(f"Print the version of %(prog)s"
                              f" (currently {__version__})"))
    parser.add_argument('files', nargs='*', default=[],
                        metavar="FILE", help="Files to move.")
    parser.add_argument('-e', '--editor', default=None, type=str,
                        help="Use EDITOR as the editor.")
    parser.add_argument('-E', '--stream-editor', default=None, type=str,
                        help="Use EDITOR as a stream editor.")

    parser.add_argument('--no-interactive', dest='interactive',
                        action='store_false', default=False)
    parser.add_argument('-i', '--interactive', dest='interactive',
                        action='store_true',
                        help="Enter menu before applying (default: no).")

    glevel = parser.add_mutually_exclusive_group()
    glevel.add_argument('-l', '--levels', default=1, type=int,
                        help="Set max directory recursion level.")
    glevel.add_argument('-d', action='store_const', const=0, dest='levels',
                        help="Same as `--levels=0'.")
    glevel.add_argument('-r', action='store_const', const=200, dest='levels',
                        help="Recurse infinitely.")
    glevel.set_defaults(levels=1)
    return parser


def get_editor(args):
    if args.stream_editor is not None:
        return args.stream_editor.lstrip(), True
    if args.editor is not None:
        return args.editor.lstrip(), False
    return None, False


def main():
    from mved.realfs import RealFs

    args = make_argparse().parse_args()

    editor, streamed = get_editor(args)

    colors = colors_for_file(sys.stdout)

    if not args.files and args.levels <= 0:
        print("cannot use -d without files", file=sys.stderr)
        return 1

    from mved.fscache import FsCache
    ed = MvEd(FsCache(RealFs()))
    try:
        if not args.files:
            ed.add_files(".", levels=args.levels)
        else:
            ed.add_files(*args.files, levels=args.levels)
    except SourceFilenameError as e:
        print(f"invalid filename: {e}", file=sys.stderr)
        return 1
    ed.apply_sourceset()
    if not ed.files:
        print("no files")
        if ed.have_error:
            return 1
        return 0

    with setup_terminal():
        if not ed.start_editor(program=editor, stream=streamed):
            # editor failed
            return 1

        from mved.menu import Menu
        menu = Menu(ed, colors=colors, always_interact=args.interactive,
                    default_editor_command=args.editor)
        menu.previous_choice = "edit"

        while not menu.do_quit:
            menu.loop()
        if menu.quit_error:
            return 1
        return 0


# vim:set sw=4 et:
