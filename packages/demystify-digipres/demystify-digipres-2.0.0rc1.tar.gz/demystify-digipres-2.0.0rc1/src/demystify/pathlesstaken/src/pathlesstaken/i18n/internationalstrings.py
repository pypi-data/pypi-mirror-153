# -*- coding: utf-8 -*-

"""International Strings.py

Module to be build up over time to make strings in output more
international.
"""


class AnalysisStringsEN:
    """Encapsulate a set of strings that can be replaced in code to make
    the output understandable in other languages.
    """

    FNAME_CHECK_ASCII = "contains, characters outside of ASCII range"
    FNAME_CHECK_PERIOD = "has a period '.' as its last character"
    FNAME_CHECK_NOT_RECOMMENDED = "contains, non-recommended character"
    FNAME_CHECK_NON_PRINT = "contains, non-printable character"
    FNAME_CHECK_RESERVED = "contains, reserved name"
    FNAME_CHECK_SPACE = "has a SPACE as its last character"
