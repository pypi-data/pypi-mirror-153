# -*- coding: utf-8 -*-

"""pathlesstaken

Module that implements checks against the Microsoft Recommendations for
file naming, plus additional recommended analyses documented below.

First created based on the recommendations here:
    http://msdn.microsoft.com/en-us/library/aa365247(VS.85).aspx

First available in:
    https://github.com/exponential-decay/droid-siegfried-sqlite-analysis-engine

"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import sys

from . import names
from .i18n.internationalstrings import AnalysisStringsEN as IN_EN


class PathlesstakenAnalysis(object):
    """PathlesstakenAnalysis

    Class to encapsulate the functionality that can be accessed via this
    module. All functions are documented further below.
    """

    def __init__(self):
        """Class initialization."""
        self.report = ""
        self.STRINGS = IN_EN

    def _clear_report(self):
        self.report = ""

    def complete_file_name_analysis(self, string, folders=False, verbose=False):
        """Run all analyses over a string object. The analyses are as follows:

        * detect_non_ascii_characters
        * detect_non_recommended_characters
        * detect_non_printable_characters
        * detect_microsoft_reserved_names
        * detect_spaces_at_end_of_names
        * detect_period_at_end_of_name

        """
        self._clear_report()
        self.verbose = verbose
        self.detect_non_ascii_characters(string, folders)
        self.detect_non_recommended_characters(string, folders)
        self.detect_non_printable_characters(string)
        self.detect_microsoft_reserved_names(string)
        self.detect_spaces_at_end_of_names(string, folders)
        self.detect_period_at_end_of_name(string, folders)
        return self.report

    def _report_issue(self, string, message, value, folders=False):
        """Helper function to build the report to return to the caller."""
        text = "File"
        if folders:
            text = "Directory"
        if not value:
            self.report = "{}{}: '{}' {}\n".format(self.report, text, string, message)
            return
        self.report = "{}{}: '{}' {} '{}'\n".format(
            self.report, text, string, message, value
        )

    @staticmethod
    def _unicodename(char):
        """Return a Unicode name for the character we want to return
        information about.
        """
        try:
            name = names.Lookup().name(char)
            return "%s: %s" % (name, char)
        except TypeError:
            if char >= 0 and char <= 31:
                return "<control character>"
            return "non-specified error"

    def detect_non_ascii_characters(self, string, folders=False):
        """Detect characters outside of an ASCII range. These are more
        difficult to preserve in today's systems, even still, though it is
        getting easier.
        """
        match = any(ord(char) > 128 for char in string)
        if match:
            for char in string:
                if ord(char) <= 128:
                    continue
                self._report_issue(
                    string=string,
                    message="{}:".format(self.STRINGS.FNAME_CHECK_ASCII),
                    value="{}, {}".format(hex(ord(char)), self._unicodename(char)),
                    folders=folders,
                )
                if not self.verbose:
                    break

    def detect_non_recommended_characters(self, string, folders=False):
        """Detect characters that are not particularly recommended. These
        characters for example a forward slash '/' often have other meanings
        in computer systems and can be interpreted incorrectly if not handled
        properly.
        """
        charlist = ["<", ">", '"', "?", "*", "|", "]", "["]
        if not folders:
            charlist = charlist + [":", "/", "\\"]
        for char in string:
            if char in charlist:
                self._report_issue(
                    string=string,
                    message="{}:".format(self.STRINGS.FNAME_CHECK_NOT_RECOMMENDED),
                    value=("{}, {}".format(hex(ord(char)), self._unicodename(char))),
                    folders=folders,
                )
                if not self.verbose:
                    break

    def detect_non_printable_characters(self, string, folders=False):
        """Detect control characters below 0x20 in the ASCII table that cannot
        be printed. Examples include ESC (escape) or BS (backspace).
        """
        for char in range(0x20):
            if chr(char) in string:
                self._report_issue(
                    string=string,
                    message="{}:".format(self.STRINGS.FNAME_CHECK_NON_PRINT),
                    value="{}, {}".format(hex(char), self._unicodename(char)),
                    folders=folders,
                )
                if not self.verbose:
                    break

    def detect_microsoft_reserved_names(self, string):
        """Detect names that are considered difficult on Microsoft file
        systems. There is a special history to these characters which can be
        read about on this link below:

            * http://msdn.microsoft.com/en-us/library/aa365247(VS.85).aspx

        """
        microsoft_reserved_names = [
            "CON",
            "PRN",
            "AUX",
            "NUL",
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "COM5",
            "COM6",
            "COM7",
            "COM8",
            "COM9",
            "LPT1",
            "LPT2",
            "LPT3",
            "LPT4",
            "LPT5",
            "LPT6",
            "LPT7",
            "LPT8",
            "LPT9",
        ]
        for reserved in microsoft_reserved_names:
            if reserved in string[0 : len(reserved)]:
                problem = True
                # If the reserved name is followed by an extension that's still
                # a bad idea.
                try:
                    if string[len(reserved)] == ".":
                        problem = True
                except IndexError:
                    # This is an exact reserved name match.
                    problem = True
                if problem:
                    self._report_issue(
                        string=string,
                        message=self.STRINGS.FNAME_CHECK_RESERVED,
                        value=reserved,
                    )

    def detect_spaces_at_end_of_names(self, string, folders=False):
        """Detect spaces at the end of a string. These spaces if ignored can
        lead to incorrectly matching strings, e.g. 'this ' is different to
        'this'.
        """
        if string.endswith(" "):
            self._report_issue(
                string=string,
                message=self.STRINGS.FNAME_CHECK_SPACE,
                value=None,
                folders=folders,
            )

    def detect_period_at_end_of_name(self, string, folders=False):
        """Detect a full-stop at the end of a name. This might indicate a
        missing file extension."""
        if string.endswith("."):
            self._report_issue(
                string=string,
                message=self.STRINGS.FNAME_CHECK_PERIOD,
                value=None,
                folders=folders,
            )

    def _detect_invalid_characters_test(self):
        """Function to help with testing until there are unit tests."""
        test_strings = [
            "COM4",
            "COM4.txt",
            ".com4",
            "abcCOM4text",
            "AUX",
            "aux",
            "abc.com4.txt.abc",
            "con",
            "CON",
            "consumer",
            "space ",
            "period.",
            "\u00F3",
            "\u00E9",
            "\u00F6",
            "\u00F3\u00E9\u00F6",
            "file[bracket]one.txt",
            "file[two.txt",
            "filethree].txt",
            '-=_|"',
            '(<>:"/\\?*|\x00-\x1f)',
        ]
        for string in test_strings:
            report = self.complete_file_name_analysis(
                string, folders=False, verbose=True
            )
            if report:
                print(report.strip())


def main():
    """pathlesstaken is a script to identify strings that when interpreted as
    file paths might prove more difficult to look after and preserve. The
    example given previously was special Microsoft reserved names. Other
    examples might include non-ASCII characters in a horrendously ASCII biased
    world.

    Notes: Running this code via main will output the most information possible
    about a string. The function complete_file_name_analysis can be called on
    the module level (or all other analysis functions) with verbose reporting
    turned off if the caller would like to see just the first instance of a
    string that might need additional processing attention, i.e. as a flag that
    there is something to look at.
    """
    try:
        cmd = " ".join(sys.argv[1:])
    except UnicodeDecodeError:
        cmd = "".join([arg.decode("utf8") for arg in sys.argv[1:]])
    if cmd.lower() == "test" and not os.path.isfile(cmd):
        print(
            "Running non-file test mode only, please use a string without 'test' in it.",
            file=sys.stderr,
        )
        PathlesstakenAnalysis()._detect_invalid_characters_test()
        return
    analysis = PathlesstakenAnalysis().complete_file_name_analysis(
        cmd, folders=False, verbose=True
    )
    if analysis:
        print(analysis.strip(), file=sys.stdout)
        sys.exit(1)
    print(
        "Analysis did not return any particular digital preservation considerations for name:",
        cmd,
        analysis.strip(),
        file=sys.stdout,
    )


if __name__ == "__main__":
    main()
