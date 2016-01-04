# -*- Mode: python; indent-tabs-mode: nil; c-basic-offset: 4; tab-width: 4 -*-
#
# Copyright (c) 2013 Giovanni Campagna <scampa.giovanni@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the GNOME Foundation nor the
#     names of its contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from gi.repository import GLib, GObject, Gtk

import util
from grid import Grid

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, title=None, default_width=1000, default_height=800, **kw):
        if not title:
            title = GLib.get_application_name()

        super().__init__(title=title, default_width=default_width, default_height=default_height, **kw)

        util.init_actions(self, [{ 'name': 'about', 'activate': self._about }])

        self.builder = Gtk.Builder()
        self.builder.add_from_resource('/org/madbob/Assetxplorer/main.ui')

        self.set_titlebar(self.builder.get_object('main-header'))
        self.new_button = self.builder.get_object('new-button')
        self.new_button.connect('clicked', self._on_new_folder)
        self.back_button = self.builder.get_object('back-button')
        self.back_button.connect('clicked', self._on_back)

        self.stack = self.builder.get_object('main-stack')
        self.add(self.stack)
        self.stack.show_all()

        self.viewer = self.builder.get_object('contents')

        self.folderslist = self.builder.get_object('list')
        self.folderslist.get_style_context().add_class("assetxplorer-folders")
        self.folderslist.connect('row-activated', self._view_folder)

        self.conf = util.get_settings('org.madbob.Assetxplorer')
        folders = self.conf.get_value('folders')
        if folders:
            self.stack.set_visible_child(self.folderslist)
            for f in folders:
                self._create_button(f)
        else:
            empty = self.builder.get_object('empty')
            self.stack.set_visible_child(empty)

    def _about(self, action, parameter):
        aboutDialog = Gtk.AboutDialog(
            authors=[ 'Roberto Guido <bob@linux.it>' ],
            translator_credits=_("translator-credits"),
            program_name=_("Assetxplorer"),
            comments=_(""),
            copyright='Copyright 2015 Roberto Guido',
            license_type=Gtk.License.GPL_3_0,
            logo_icon_name=pkg.name,
            version=pkg.version,
            website='atx.madbob.org',
            wrap_license=True,
            modal=True,
            transient_for=self
        )

        aboutDialog.show()
        aboutDialog.connect('response', lambda dialog, id: dialog.destroy())

    def _view_folder(self, list, button):
        for child in self.viewer.get_children():
            self.viewer.remove(child)

        path = button.get_children()[0].get_label()
        grid = Grid(path)
        self.viewer.pack_start(grid, True, True, 0)

        self.stack.set_visible_child(self.viewer)
        self.new_button.set_visible(False)
        self.back_button.set_visible(True)

        self.viewer.show_all()

    def _create_button(self, buttonname):
        button = Gtk.ListBoxRow()
        button.get_style_context().add_class("assetxplorer-folder")
        button.add(Gtk.Label(buttonname))
        self.folderslist.add(button)
        button.show_all()
        self.stack.set_visible_child(self.folderslist)
        return button

    def _add_folder(self, foldername):
        folders = self.conf.get_value('folders')
        folders_array = folders.unpack()

        if foldername not in folders_array:
            self.conf.set_value('folders', GLib.Variant("as", folders_array + [foldername]))
            self._create_button(foldername)

    def _on_new_folder(self, button):
        filechooserdialog = Gtk.FileChooserDialog(parent=self, title=_("Choose a Folder to Explore"), action=Gtk.FileChooserAction.SELECT_FOLDER, buttons=(Gtk.STOCK_OK, Gtk.ResponseType.OK))
        response = filechooserdialog.run()
        if response == Gtk.ResponseType.OK:
            self._add_folder(filechooserdialog.get_filename())
        filechooserdialog.destroy()

    def _on_back(self, button):
        self.grid = None
        self.stack.set_visible_child(self.folderslist)
        self.new_button.set_visible(True)
        self.back_button.set_visible(False)
