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

import getopt
import sys
import os
import gtk
import pygame

SCREEN_WIDTH = 900
ARBITRARY_LARGE_HEIGHT = 10000
JPEG_QUALITY = 80

def resize_image(filename):

    print '%s file size before conversion: %d KB' %  (filename, os.stat(filename).st_size / 1024)
    im = pygame.image.load(filename)
    image_width, image_height = im.get_size()
    print '%s image size before conversion: %d x %d' %  (filename,   image_width,  image_height)
    resize_to_width = SCREEN_WIDTH
    if image_width <= SCREEN_WIDTH:
        resize_to_width = image_width
    try:
        scaled_pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, resize_to_width, ARBITRARY_LARGE_HEIGHT)
        scaled_pixbuf.save(filename + '.jpg', "jpeg", {"quality":"%d" % JPEG_QUALITY})
    except:
        print 'File could not be converted'
    print '%s file size after conversion %d KB' % (filename, os.stat(filename + '.jpg').st_size /1024)
    im = pygame.image.load(filename + '.jpg')
    image_width, image_height = im.get_size()
    print '%s image size after conversion: %d x %d' % (filename + '.jpg',  image_width,  image_height)
    print ''
    return

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "")
        i = 0
        while i < len(args):
            success = resize_image(args[i])
            i = i + 1
    except getopt.error, msg:
        print msg
        print "This program has no options"
        sys.exit(2)
