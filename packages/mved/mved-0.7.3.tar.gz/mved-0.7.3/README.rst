****
mved
****

Bulk-move, copy and delete files safely using a text editor.
############################################################

- Verifies validity of changes before anything is applied.
- No restrictions for encoding in filenames. ASCII control characters and
  invalid UTF-8 are escaped.
- Deletions can be reverted until the menu is closed.
- Fully interactive mode allows reverting any changes until menu is closed.
- In case an error occurs (e.g. insufficient permissions) any changes can be
  reverted.

Installing
==========

- From PyPI: run ``pip install mved`` (`view on pypi.org`_)
- From Arch User Repository (AUR): package ``mved`` (`view in AUR`_)

.. _`view on pypi.org`: https://pypi.org/project/mved/
.. _`view in AUR`: https://aur.archlinux.org/packages/mved

Basic Usage
===========

Pass files to rename to ``mved``::

  mved *.txt

An editor (``$VISUAL`` or ``$EDITOR``) is started with a list of files::

  1 one.txt
  2 two.txt

Every filename is listed with a number separated by a single space.

- To rename or move a file, change its path after the number.
- To copy a file, duplicate the line including the number and change the path.
  The original can be preserved or moved as well.
- To delete a file, delete the line including the number.
- Lines starting with ``#`` are ignored, so adding ``#`` before the number
  would also delete it.

After saving the file and closing the editor, if the changes are valid, the
modifications are applied immediately.
If there were no deletions, ``mved`` exits.

If there were deletions, the menu is shown::

  [revert/dryrun/quit] >

No files were deleted yet, only moved to a temporary location.

- ``revert`` immediately reverts all files to their original locations.
- ``dryrun`` prints what ``revert`` would do without touching files.
- ``quit`` closes the menu and finally deletes any files that were removed with
  the editor. Pressing CTRL-D is equivalent to ``quit``.

Menu
====

The menu is skipped in most cases. To enter the menu after every command, pass
``-i``/``--interactive`` to ``mved``.

Available commands are listed in the prompt. Which commands are available
depends on the current state.

Some commands have an upper-case variant. If any character in the entered
command is upper-case, these commands provide a slightly different function.

Commands
--------

- ``apply``: Apply the changes made with the editor. This is usually done
  automatically unless ``-i``/``--interactive`` was specified.

  - If upper-case: If all changes were successful, apply deletions immediately
    and close the program.
- ``dryrun``: Print the changes ``apply`` would make without applying any
  changes.
- ``edit``: Start the editor again with the current file list.

  For entries to be moved or deleted, the original line is added as a comment.
  These comments are ignored by the parser.

  - If upper-case: do not include the comments for changed entries.
  - The editor to run can be specified after the command. See `Editor`_ below.
    For example, the file list can be opened with ``vi`` by entering::

      edit vi

    If the command is preceded by ``|`` (pipe) then the command is run as a
    stream editor. See `Stream Editor`_ below. For example, to replace every
    occurrence of ``one`` with ``two``, enter::

      edit |sed s/one/two/

    If the command is omitted, the it is taken from the ``-e``/``--editor``
    option, ``$VISUAL``, or ``$EDITOR``, (the first one that is set) or ``vi``.
- ``reset``: Run the editor with the original file list. If no changes are
  made, the previous changes are restored.

  - If upper-case: Immediately remove all changes of the file list, without
    running the editor.
  - If lower-case: The editor program can be specified like with ``edit``.
- ``diff``: Print a list of differences made to the file list.

  - If upper-case: Show file numbers in the diff.
- ``add``: See `file exists`_ conflict below.
- ``conflicts``: Print the list of conflicts again.

  - If upper-case: Use a different format that includes file numbers and
    doesn't abbreviate long lists.
- ``revert``: Revert the changes of the last ``apply`` command. Files marked
  for deletion are moved back to their source location.

  - If used after an error during ``apply``, the partial changes so far made by
    ``apply`` are reverted.
  - If an error occurs during ``revert``, the next ``revert`` will restore
    files to the locations before the failed ``revert`` command. This indicates
    other programs are making changes concurrently to ``mved``. Use external
    programs to resolve these conflicts and make sure no other programs make
    concurrent changes.
- ``quit``: Exit the program. If changes have been applied successfully and
  there were deletions, files marked for deletion are irrevocably deleted.

  - If used after an error during ``apply``, additional confirmation is
    required to quit without reverting.
  - Unless used after an error during ``apply``, pressing CTRL-D is equivalent
    to ``quit``.

Commands don't need to be typed out in full: when the prefix of a command is
entered, the first command matching that prefix is executed.

For example, given the prompt ``[diff/apply/dryrun/edit/reset/quit] >``,
to run the given commands the following input could be entered:

- lower-case ``diff``::

    diff
    d

- lower-case ``dryrun``::

    dryrun
    dry
    dr

- upper-case ``edit``::

    EDIT
    Edit
    eDit
    edI
    E

Conflicts
=========

After editing the file list, conflicts may be detected and the changes cannot
be applied. In that case, the conflicts are listed and the menu is shown::

  [conflicts/diff/edit/reset/quit] >

No changes have been applied yet. Enter ``edit`` to resolve conflicts by
editing the file list. See Menu_ for further usage.

The following kinds of conflicts may be detected:

- ``destination conflict``

  Two files in the list have the same destination filename.

  Enter ``edit`` to resolve the conflicts in the editor.

.. _`file exists`:

- ``file exists``

  A destination file already exists that was not passed to ``mved``. Enter
  ``add`` to add the destination files to the list and ``edit`` to resolve the
  conflicts by moving the added files.

- ``path exists``

  Part of a destination path already exists and is not a directory.

- ``invalid filename``

  A filename on the list is invalid.

  Enter ``edit`` to change invalid filenames in the editor.

- ``cannot copy/delete directory``

  Copying and deleting whole directories is not supported.

- ``directory conflict``

  A modified directory path is part of the source or destination of other
  files. Such changes currently are not supported. Try making the changes with
  separate invocations of ``mved``.

Escapes
=======

ASCII control characters and invalid UTF-8 are converted to an escaped
representation in the file list.

Escape sequences are initiated with the \\ (backslash) character. Anything else
is left unmodified. Literal backslashes in filenames must be doubled.

The replaced control characters are:

- ``0-31`` (``0`` to ``0x1f`` inclusive)
- ``127`` (``0x7f``)

The following table lists available escape sequences. The `Escape` column lists
the escape sequence understood by ``mved``. All other columns are for reference
only.

+----------+-------+----------+-----+-----+-----------------------------+
| Escape   | Abbr. | Caret    | Hex | Dec | Description                 |
|          |       | Notation |     |     |                             |
+==========+=======+==========+=====+=====+=============================+
| ``\a``   | BEL   | ``^G``   |  07 |   7 | Bell                        |
+----------+-------+----------+-----+-----+-----------------------------+
| ``\b``   | BS    | ``^H``   |  08 |   8 | Backspace                   |
+----------+-------+----------+-----+-----+-----------------------------+
| ``\t``   | TAB   | ``^I``   |  09 |   9 | Horizontal Tabulation (Tab) |
+----------+-------+----------+-----+-----+-----------------------------+
| ``\n``   | LF    | ``^J``   |  0a |  10 | Line Feed                   |
+----------+-------+----------+-----+-----+-----------------------------+
| ``\v``   | VT    | ``^K``   |  0b |  11 | Vertical Tabulation         |
+----------+-------+----------+-----+-----+-----------------------------+
| ``\f``   | FF    | ``^L``   |  0c |  12 | Form Feed                   |
+----------+-------+----------+-----+-----+-----------------------------+
| ``\r``   | CR    | ``^M``   |  0d |  13 | Carriage Return             |
+----------+-------+----------+-----+-----+-----------------------------+
| ``\\``   |       |          |  5c |  92 | Backslash                   |
+----------+-------+----------+-----+-----+-----------------------------+
| ``\x00`` |       |          | 00  | 0   | Arbitrary octet             |
| \..      |       |          | \.. | \.. |                             |
| ``\xff`` |       |          | ff  | 255 |                             |
+----------+-------+----------+-----+-----+-----------------------------+

Any byte value can be specified with ``\x`` followed by two hexadecimal digits
representing its value, ranging from ``\x00`` to ``\xff``.

Note that ``\x`` escape sequences specify literal octets and are not encoded to
UTF-8. Values above ``\x7f`` will result in invalid UTF-8 unless constructed in
a conforming manner. To specify code points above ``U+007F``, enter literal
UTF-8 in the editor.

Note that even though ``\x00`` can be specified, it is not allowed in
filenames.

Advanced Options
================

Interactive Mode
----------------

Passing ``-i``/``--interactive`` to ``mved`` starts interactive mode. In this
mode, the menu is shown after every action. After editing, changes can be
inspected with ``diff`` or ``dryrun``, edited with ``edit`` or ``reset`` or
accepted with ``apply``. After ``apply``, all changes can be undone with
``revert``, even if there were no deletions.

Recursion Depth
---------------

The ``-l``/``--levels``, ``-d``, and ``-r`` options control the recursion depth
for directories passed to ``mved``.

- ``-l``/``--levels`` sets the recursion depth to the given number.

  The default is ``1``. This means for files passed to ``mved`` that are
  directories, the contained files are added.
- ``-r`` recurses infinitely. All files in the hierarchy are listed.
- ``-d`` disables recursion. This can be used to rename given directories.

Editor
------

The ``-e``/``--editor`` option specifies the interactive editor command. It is
also used when entering the ``edit`` and ``reset`` menu commands without
argument. The default is taken from the environment:

- ``$VISUAL`` is used, if it is set.
- Otherwise, ``$EDITOR`` is used, if it is set.
- If both are unset, ``vi`` is used.

The command is run with ``/bin/sh``. The file to edit is added as the last
argument.

Stream Editor
-------------

The ``-E``/``--stream-editor`` option or entering ``edit |<command>`` in the
menu runs the given command as a stream editor. The command receives the file
list on its `stdin` and must print the result to `stdout`. The format is the
same as with the interactive editor. The command is run with ``/bin/sh``.

For example, to replace all occurrences of ``one`` with ``two``, run::

  mved -E 'sed s/one/two' *.txt

This is only applied on startup, in place of the initial interactive editor
call.

To do the same in the menu, enter
::

  edit |sed s/one/two
