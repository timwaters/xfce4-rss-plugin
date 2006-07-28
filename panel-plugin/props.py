# xfce4-rss-plugin - an RSS aggregator for the Xfce 4 Panel
# Copyright (c) 2006 Adriano Winter Bess <adriano@xfce.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License ONLY.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import pygtk
pygtk.require("2.0")
import gtk
import gobject
from gettext import gettext as _

class PropertiesDialog (gtk.Dialog):
    def __init__ (self, config):
        gtk.Dialog.__init__ (self, _("RSS Aggregator"),
                             None, gtk.DIALOG_MODAL|gtk.DIALOG_NO_SEPARATOR,
                             (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
        self.config = config
        self.set_border_width (8)
        self.vbox.set_homogeneous (False)
        self.set_default_size (600, 400)

        model = gtk.ListStore (gobject.TYPE_STRING, gobject.TYPE_STRING)
        for feed in config.traverse_feeds ():
            model.append ((feed['name'], feed['url']))
        self.build_view (model)

        vb = gtk.VBox (spacing=8)
        but = gtk.Button (stock=gtk.STOCK_ADD)
        but.connect ("clicked", add_cb, self.feeds_view)
        vb.pack_start (but, False)
        but = gtk.Button (stock=gtk.STOCK_REMOVE)
        but.connect ("clicked", remove_cb, self.feeds_view)
        vb.pack_start (but, False)

        lab = gtk.Label (_("RSS Feeds:"))
        lab.set_alignment (0.0, 0.5)
        self.vbox.pack_start (lab, False)
        hb = gtk.HBox (spacing=8)
        hb.pack_start (self.feeds_view)
        align = gtk.Alignment (0.5, 0.5)
        align.add (vb)
        hb.pack_start (align, False)
        self.vbox.pack_start (hb)

        self.connect ("response", response_cb, None)

    def build_view (self, model):
        tv = gtk.TreeView (model)
        tv.set_headers_visible (True)
        tv.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

        col = gtk.TreeViewColumn (_("Name"))
        cell = gtk.CellRendererText ()
        cell.set_property ("editable", True)
        cell.connect ("edited", edited_cb, (model, 0))
        col.pack_start (cell)
        tv.append_column (col)
        col.set_attributes (cell, text=0)
        col.set_sort_column_id (0)
        tv.set_search_column (0)

        col = gtk.TreeViewColumn (_("URL"))
        cell = gtk.CellRendererText ()
        cell.set_property ("editable", True)
        cell.connect ("edited", edited_cb, (model, 1))
        col.pack_start (cell)
        tv.append_column (col)
        col.set_attributes (cell, text=1)

        self.feeds_view = tv

def response_cb (dlg, rid, dummy):
    model = dlg.feeds_view.get_model ()
    dlg.config.clear_feeds ()
    for feed in model:
        dlg.config.add_feed (feed[0], feed[1])
    dlg.config.write_config ()
    dlg.destroy ()

def edited_cb (cell, path, text, data):
    model, column = data
    model[path][column] = text

def remove_cb (but, feeds_view):
    selection = feeds_view.get_selection ()
    if selection.count_selected_rows () > 0:
        (model, rows) = selection.get_selected_rows ()
        refs = list ()
        for path in rows:
            refs.append (gtk.TreeRowReference (model, path))
        for ref in refs:
            model.remove (model.get_iter (ref.get_path ()))

def add_cb (but, feeds_view):
    model = feeds_view.get_model ()
    model.append ((_("Name"), "http://"))
