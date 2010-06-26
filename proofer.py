#! /usr/bin/env python
#
# proofer.py
# Copyright (C) 2010  James D. Simmons
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
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

import sys
import os
import gtk
import getopt
import pango

page=0
IMAGE_WIDTH = 600
ARBITRARY_LARGE_HEIGHT = 10000

class Proofer():

    def keypress_cb(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'F10':
            self.font_increase()
            return True
        if keyname == 'F9':
            self.font_decrease()
            return True
        if keyname == 'Page_Up' :
            self.page_previous()
            return True
        if keyname == 'Page_Down':
            self.page_next()
            return True
        return False

    def font_decrease(self):
        font_size = self.font_desc.get_size() / 1024
        font_size = font_size - 1
        if font_size < 1:
            font_size = 1
        self.font_desc.set_size(font_size * 1024)
        self.textview.modify_font(self.font_desc)

    def font_increase(self):
        font_size = self.font_desc.get_size() / 1024
        font_size = font_size + 1
        self.font_desc.set_size(font_size * 1024)
        self.textview.modify_font(self.font_desc)

    def page_previous(self):
        global page
        self.save_current_file(self.filenames[page])
        page=page-1
        if page < 0: page=0
        self.read_file(self.filenames[page])
        self.show_image(self.filenames[page])

    def page_next(self):
        global page
        self.save_current_file(self.filenames[page])
        page=page+1
        if page >= len(self.filenames): page=0
        self.read_file(self.filenames[page])
        self.show_image(self.filenames[page])

    def read_file(self, filename):
        "Read the text file"
        text_filename = self.find_text_file(filename)
        self.window.set_title("Proofer " + filename)
        etext_file = open(text_filename,"r")
        textbuffer = self.textview.get_buffer()
        text = ''
        line = ''
        while etext_file:
            line = etext_file.readline()
            if not line:
                break
            text = text + unicode(line, 'iso-8859-1')
        text = text.replace("'I`",  'T')
        text = text.replace("'|`",  'T')
        text = text.replace("l`",  'f')
        text = text.replace("I`",  'f')
        text = text.replace("t`",  'f')
        text = text.replace("ll",  'H')
        textbuffer.set_text(text)
        self.textview.set_buffer(textbuffer)
        etext_file.close()

    def find_text_file(self, filename):
        filename_tuple = filename.split('.')
        text_filename = filename_tuple[0] + '.txt'
        text_filename = '../text/' + text_filename
        return text_filename

    def save_current_file(self, filename):
        text_filename = self.find_text_file(filename)
        f = open(text_filename, 'w')
        textbuffer = self.textview.get_buffer()
        text =  textbuffer.get_text(textbuffer.get_start_iter(),  
                                    textbuffer.get_end_iter())
        try:
            f.write(text)
        finally:
            f.close
        return True


    def show_image(self, filename):
        "display a resized image in a full screen window"
        scaled_pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 
                            IMAGE_WIDTH, ARBITRARY_LARGE_HEIGHT)
        self.image.set_from_pixbuf(scaled_pixbuf)
        self.image.show()

    def destroy_cb(self, widget, data=None):
        self.save_current_file(self.filenames[page])
        gtk.main_quit()

    def main(self, args):
        self.filenames = args
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy_cb)
        self.window.set_title("Proofer " + args[0])
        self.window.set_size_request(1200, 600)
        self.window.set_border_width(0)
        self.scrolled_window = gtk.ScrolledWindow(
                                                  hadjustment=None, \
                                                  vadjustment=None)
        self.scrolled_window.set_policy(gtk.POLICY_NEVER, 
                                        gtk.POLICY_AUTOMATIC)
        self.textview = gtk.TextView()
        self.textview.set_editable(True)
        self.textview.set_left_margin(50)
        self.textview.set_cursor_visible(True)
        self.textview.connect("key_press_event", 
                              self.keypress_cb)
        self.font_desc = pango.FontDescription("courier 12")
        self.textview.modify_font(self.font_desc)
        self.scrolled_window.add(self.textview)
        self.read_file(args[0])
        self.textview.show()
        self.scrolled_window.show()
        self.window.show()
        
        self.scrolled_image = gtk.ScrolledWindow()
        self.scrolled_image.set_policy(gtk.POLICY_NEVER, 
                                       gtk.POLICY_AUTOMATIC)
        self.image = gtk.Image()
        self.image.show()
        self.show_image(args[0])
        self.scrolled_image.add_with_viewport(self.image)
        
        self.hpane = gtk.HPaned()
        self.hpane.add1(self.scrolled_window)
        self.hpane.add2(self.scrolled_image)
        self.hpane.show()

        self.window.add(self.hpane)
        self.scrolled_window.show()
        self.scrolled_image.show()
        self.window.show()

        gtk.main()
      
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "")
        Proofer().main(args)
    except getopt.error, msg:
        print msg
        print "This program has no options"
        sys.exit(2)
