# -*- coding: utf-8 -*-

"""
Copyright (c) 2014, Cooper Hewitt Smithsonian Design Museum
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the {organization} nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import absolute_import, print_function, unicode_literals

import logging
import sys

LOGFORMAT = (
    "%(asctime)-15s %(levelname)s: %(filename)s:%(lineno)s:%(funcName)s(): %(message)s"
)
DATEFORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(format=LOGFORMAT, datefmt=DATEFORMAT, level="INFO")

from . import ucd


class Lookup(object):
    """Class responsible for lookup of Unicode character names."""

    def __init__(self):
        """Class initialization."""
        pass

    @staticmethod
    def name(char):
        """Return a name for a given character from the Cooper-Hewitt name
        lookup.
        """
        id_ = ord(char)
        hex_ = "%04X" % id_
        logging.debug("INFO: char: %s id: %s hex: %s" % (char, id_, hex_))
        return ucd.UCD_MAP.get(hex_, None)


def main():
    """Primary entry point for this script."""
    try:
        cmd = " ".join(sys.argv[1:])
    except UnicodeDecodeError:
        cmd = "".join([arg.decode("utf8") for arg in sys.argv[1:]])
    ref = Lookup()
    for char in cmd:
        name = ref.name(char)
        print("%s is %s" % (char, name))


if __name__ == "__main__":
    main()
