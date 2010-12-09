#! /usr/bin/env python

# Copyright (C) 2010 James D. Simmons
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import glob
import getopt
import sys
import subprocess

def run_tesseract(filename):

    filename_tuple = filename.split('.')
    filename_base = filename_tuple[0]
    subprocess.call(["tesseract", filename, filename_base])
    print 'filename', filename
    return

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "")
        if len(args) == 1:
            print 'using glob'
            args = glob.glob(args[0])
            args.sort()
        i = 0
        while i < len(args):
            run_tesseract(args[i])
            i = i + 1
    except getopt.error, msg:
        print msg
        print "This program has no options"
        sys.exit(2)
