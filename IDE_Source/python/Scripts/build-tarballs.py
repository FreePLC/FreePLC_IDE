#!c:\python27\python.exe

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

# This script is not meant to be distributed to users of Twisted.
# It is only for use in making upstream Twisted releases.

import sys

from twisted.python._release import BuildTarballsScript

BuildTarballsScript().main(sys.argv[1:])
