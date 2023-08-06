# This file is part of mved, the bulk file renaming tool.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

"""Menu interaction."""

import readline
import sys

from mved.colors import NO_COLORS
from mved.utils import InternalError

# suppress unused warning
readline


def commonprefix(*args):
    "Given a list of pathnames, returns the longest common leading component"
    if not args:
        return ''
    s1 = min(args)
    s2 = max(args)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
    return s1


def ischoice(instr, choice):
    return len(instr) and commonprefix(instr, choice) == instr


def readchoice(choices, abortchoice=None,
               hchoices=[], format=None, sep=None):
    if format is None:
        format = "[{choices}] > "
    if sep is None:
        sep = "/"
    prompt = format.format(choices=sep.join(choices))
    abort = False
    try:
        instr = input(prompt)
    except UnicodeError as e:
        print(e)
        instr = ''
    except KeyboardInterrupt:
        abort = True
    except EOFError:
        abort = True
    if abort:
        if abortchoice is None:
            # add missing newline after prompt
            print()
            return None, False, ''
        else:
            instr = abortchoice
            print(instr)
    instr = instr.lstrip()
    cmd, _, _ = instr.partition(" ")
    lower = cmd.lower()
    isupper = lower != cmd
    for c in choices + hchoices:
        if ischoice(lower, c):
            return c, isupper, instr
    return None, isupper, instr


class Menu(object):

    CHOICEMAP = {'revert': 'apply', 'dryrun': 'apply'}

    def __init__(self, ed, colors=NO_COLORS, always_interact=False,
                 default_editor_command=None):
        self.ed = ed
        self.colors = colors
        self.promptcolors = colors.for_readline
        self.applier = None
        self.apply_output = 'diff'
        self.always_interact = always_interact
        self.previous_choice = None
        self.printed_conflicts = False
        self._edit_successful = True
        self.default_editor_command = default_editor_command

        self.do_quit = False
        self.quit_error = False

    def _readchoice(self, choices, abortchoice=None, hchoices=[]):
        if not self.printed_conflicts:
            self.ed.write_conflicts(out=sys.stdout, colors=self.colors)
            self.printed_conflicts = True
        if self.applier:
            print(self.applier.get_stats_message(self.colors))
        else:
            print(self.ed.stats.get_message(colors=self.colors))
        colors = self.promptcolors
        if self.applier is None:
            c_prompt = colors.prompt
            c_choice = colors.promptchoice
        elif self.applier.successful:
            c_prompt = colors.successprompt
            c_choice = colors.successchoice
        else:
            c_prompt = colors.revertprompt
            c_choice = colors.revertchoice
        format = (f"{c_prompt}[{c_choice}{{choices}}"
                  f"{c_prompt}] > {colors.reset}")
        sep = f"{c_prompt}/{c_choice}"
        return readchoice(choices, abortchoice, hchoices=hchoices,
                          format=format, sep=sep)

    def _get_choices(self):
        if self.applier is None:
            choices = []
            count = self.ed.stats.change_count
            if self.ed.has_conflicts:
                choices.append("conflicts")
            if count:
                choices.append("diff")
            if not self.ed.has_conflicts and count:
                choices.append("apply")
                choices.append("dryrun")
            choices.append("edit")
            if self.ed.has_exist_conflicts:
                choices.append("add")
            if count:
                choices.append("reset")
            choices.append("quit")
            hchoices = ["recalc"]
            abortchoice = "quit"
        else:
            choices = ["revert", "dryrun", "quit"]
            hchoices = []
            if self.applier.successful:
                abortchoice = "quit"
            else:
                abortchoice = None
        return choices, hchoices, abortchoice

    def _handle_choice(self, choice, upper, chargs):
        funcname = 'choice_' + self.CHOICEMAP.get(choice, choice)
        func = getattr(self, funcname)
        if func:
            func(choice, chargs, upper)
        else:
            raise InternalError("No such choice: " + choice)

    def _try_quick_choice(self, choices):
        if self.always_interact:
            return None
        if not self.applier:
            if self.previous_choice == "edit":
                if (self.ed.stats.change_count == 0
                        and self.ed.stats.conflicts == 0):
                    print(self.ed.stats.get_message(colors=self.colors))
                    if "quit" in choices:
                        return "quit", False, "quit"
                if not self._edit_successful:
                    return None
                if self.ed.stats.files == self.ed.stats.deletes:
                    # escape hatch in case editor cannot be canceled:
                    # deleting all files always enters the menu
                    return None
                if "apply" in choices:
                    return "apply", False, "apply"
        if self.applier and self.applier.successful:
            if self.previous_choice == "apply" and self.ed.stats.deletes == 0:
                if "quit" in choices:
                    return "quit", False, "quit"
        if self.previous_choice in ("revert", "add") and "edit" in choices:
            return "edit", False, "edit"
        return None

    def loop(self):
        if not self.applier and not self.ed.calculated:
            self.ed.calculate_changes()
            self.printed_conflicts = False
        choices, hchoices, abortchoice = self._get_choices()
        choice, upper, instr = (
            self._try_quick_choice(choices)
            or self._readchoice(choices, abortchoice, hchoices)
        )
        chstr, _, chargs = instr.partition(" ")
        if choice is None:
            if chstr:
                print(f"invalid choice: {chstr}")
        else:
            self.previous_choice = choice
            self._handle_choice(choice, upper, chargs.lstrip())

    def _signal_quit(self, error=False):
        self.do_quit = True
        self.quit_error = error

    def _signal_recalc(self):
        self.ed.calculated = False

    def choice_apply(self, choice, args, upper):
        dry = choice == "dryrun"
        revert = self.applier is not None
        if revert:
            count = self.applier.num_revert_changes
            applier = self.applier.create_revert_context()
        else:
            count = self.ed.stats.change_count
            applier = self.ed.create_applier()
            applier.delete_on_success = upper
        if dry:
            modestr = "dry-run"
        elif revert:
            modestr = "reverting"
        else:
            modestr = "applying"
        print(f"{modestr} {self.colors.colorize(count, 'stats')} changes")
        out = sys.stdout
        if not dry and not revert and self.apply_output == 'diff':
            self.ed.write_diff(out, numbers=False, colors=self.colors)
            out = None
        applier.apply(out=out, dryrun=dry, colors=self.colors)
        if not dry:
            if applier.error:
                import traceback
                traceback.print_exception(*applier.error)
                if applier.num_revert_changes:
                    self.applier = applier
                    print(self.applier.get_stats_message(self.colors))
                else:
                    print("Nothing was changed.")
            elif revert:
                self.applier = self.applier.parent
                if not self.applier:
                    self._signal_recalc()
            else:
                self.applier = applier
                if upper:
                    self._signal_quit()

    def choice_edit(self, choice, args, upper, reset=False):
        stream = args.startswith("|")
        if stream:
            program = args[1:].lstrip()
            if not program:
                print("Missing program.")
                self._edit_successful = False
                return
        else:
            program = args or self.default_editor_command
        self._edit_successful = self.ed.start_editor(
            reset=reset, sources=(not upper),
            program=program, stream=stream,
        )

    def choice_reset(self, choice, args, upper):
        if upper:
            self.ed.reset()
        else:
            self.choice_edit(choice, args, False, reset=True)

    def choice_diff(self, choice, args, upper):
        self.ed.write_diff(sys.stdout, numbers=upper, colors=self.colors)

    def choice_add(self, choice, args, upper):
        self.ed.add_exist_conflict_files()

    def choice_conflicts(self, choice, args, upper):
        self.ed.write_conflicts(sys.stdout, short=(not upper),
                                colors=self.colors)

    def choice_recalc(self, choice, args, upper):
        self._signal_recalc()

    def choice_quit(self, choice, args, upper):
        if self.applier:
            if not self.applier.successful:
                promptfmt = (
                    "Errors occurred. Quit without reverting? [{choices}] ")
                choice, upper, instr = readchoice(["yes", "no"],
                                                  format=promptfmt)
                if choice == "yes":
                    self._signal_quit(error=True)
            else:
                if self.applier:
                    self.applier.delete_now()
                self._signal_quit()
        else:
            self._signal_quit()


# vim:set sw=4 et:
