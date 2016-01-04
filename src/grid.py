from gi.repository import GLib, GObject, Gtk, Gdk, GdkPixbuf, Gio
import os
import math

class Grid(Gtk.EventBox):
    def __init__(self, path):
        Gtk.EventBox.__init__(self)

        self.mainpath = path
        self.cell_size = 100
        self.stop_action = None

        self.builder = Gtk.Builder()
        self.builder.add_from_resource('/org/madbob/Assetxplorer/grid.ui')

        self.grid = self.builder.get_object('grid')
        self.grid.get_style_context().add_class("grid")
        self.scrollable_view = self.builder.get_object('scrollable').get_children()[0]
        self.add(self.builder.get_object('container'))

        self.filepath = self.builder.get_object('info-file-name')
        self.filemeta = self.builder.get_object('info-file-metadata')

        self.valid_mimetypes = []
        for fmt in GdkPixbuf.Pixbuf.get_formats():
            for m in fmt.get_mime_types():
                self.valid_mimetypes.append(m)

        self._recursive_read(self.mainpath)

    def _recursive_read(self, path):
        gfile = Gio.file_new_for_path(path)
        self.stop_action = Gio.Cancellable()
        gfile.enumerate_children_async(','.join([Gio.FILE_ATTRIBUTE_STANDARD_DISPLAY_NAME,
                                                 Gio.FILE_ATTRIBUTE_STANDARD_TYPE,
                                                 Gio.FILE_ATTRIBUTE_STANDARD_CONTENT_TYPE,
                                                 Gio.FILE_ATTRIBUTE_STANDARD_SIZE]), 0, 0, self.stop_action, self._read_folder)

    def _read_folder(self, parent, result):
        enumfiles = parent.enumerate_children_finish(result)
        self.stop_action = Gio.Cancellable()
        enumfiles.next_files_async(10, GLib.PRIORITY_DEFAULT, self.stop_action, self._enum_dir_cb, parent)

    def _enum_dir_cb(self, fileenum, result, parent):
        files = fileenum.next_files_finish(result)
        if files is None or len(files) == 0:
            return

        for f in files:
            name = f.get_attribute_string(Gio.FILE_ATTRIBUTE_STANDARD_DISPLAY_NAME)
            path = parent.get_path() + '/' + name

            t = f.get_attribute_uint32(Gio.FILE_ATTRIBUTE_STANDARD_TYPE)
            if t == Gio.FileType.DIRECTORY:
                self._recursive_read(path)
            else:
                mime = f.get_attribute_string(Gio.FILE_ATTRIBUTE_STANDARD_CONTENT_TYPE)
                if mime in self.valid_mimetypes:
                    try:
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
                        if pixbuf is not None:
                            width = pixbuf.get_width()
                            height = pixbuf.get_height()
                            resolution = "%dx%d" % (width, height)
                            size = GLib.format_size_for_display(f.get_attribute_uint64(Gio.FILE_ATTRIBUTE_STANDARD_SIZE))
                            button = self._scale_image(pixbuf)
                            button.show_all()
                            button.connect('button_press_event', self._item_selected, [path[len(self.mainpath):], size, resolution])
                    except:
                        print("Error loading %s" % path)

        self.stop_action = Gio.Cancellable()
        fileenum.next_files_async(10, GLib.PRIORITY_DEFAULT, self.stop_action, self._enum_dir_cb, parent)

    def _scale_image(self, pixbuf):
        width = pixbuf.get_width()
        height = pixbuf.get_height()

        if width > self.cell_size or height > self.cell_size:
            if width > self.cell_size:
                r = self.cell_size / width
                height = round(height * r)
                width = round(width * r)

            if height > self.cell_size:
                r = self.cell_size / height
                height = round(height * r)
                width = round(width * r)

            pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)

        elif width < self.cell_size and height < self.cell_size:
            r = self.cell_size / max(width, height)
            height = round(height * r)
            width = round(width * r)
            pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)

        button = Gtk.Button()
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        button.set_image(image)
        self.grid.add(button)

        return button

    def _item_selected(self, button, event, metadata):
        self.filepath.set_text(metadata[0])
        self.filemeta.set_text(" %s | %s " % (metadata[1], metadata[2]))
