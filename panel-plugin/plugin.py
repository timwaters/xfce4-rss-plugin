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

import pyexo
pyexo.require('0.3')
import exo

import gobject
import xfce4
from gettext import textdomain, bindtextdomain, gettext as _
import sys
from xfce4.rssplugin.globals import *
from xfce4.rssplugin.props import PropertiesDialog
from xfce4.rssplugin.config import PluginConfig
import feedparser

class RSSPlugin (xfce4.panel.Plugin):
    def __init__ (self):
        xfce4.panel.Plugin.__init__ (self)

        # The following doesn't work (pyxfce bug?)
        #xfce4.util.textdomain (NAME, LOCALEDIR, "UTF-8")
        bindtextdomain (NAME, LOCALEDIR)
        textdomain (NAME)

        path = self.lookup_rc_file ()
        new = False
        if path == None:
            path = self.save_location (True)
            new = True
        self.config = PluginConfig (path, new)

        # Start with an empty feeds menu
        self.feeds_mi = gtk.MenuItem (_("Feeds"))
        self.feeds_mi.show ()
        self.menu_insert_item (self.feeds_mi)
        self.feeds_mi.set_submenu (gtk.Menu ())
        if not new:
            self.setup_feeds_menu ()
        # Update every 30 minutes. Seriously, this should be
        # configured by the user.
        self.update_id = gobject.timeout_add (1800000, update_menu_cb, self)

        refresh_mi = gtk.MenuItem (_("Refresh all"))
        refresh_mi.connect ("activate", lambda refresh_mi_fn: update_menu_cb (self))
        refresh_mi.show ()
        self.menu_insert_item (refresh_mi)
        
        label = gtk.Label (_("RSS"))
        label.show ()
        eb = gtk.EventBox ()
        eb.add (label)
        eb.set_above_child (True)
        eb.show ()
        self.add (eb)
        self.add_action_widget (eb)

        self.connect ("size-changed", size_changed_cb, None)
        self.connect ("configure-plugin", configure_cb, None)
        self.menu_show_configure ()
        self.connect ("destroy", destroy_cb, None)

    def setup_feeds_menu (self):
        feeds_menu = gtk.Menu ()
        
        for feed in self.config.traverse_feeds ():
            # Many things can go wrong here, by now simply
            # ignore everything
            try:
                feed_data = feedparser.parse (feed['url'])
            except:
                continue
            feed_mi = gtk.MenuItem (feed['name'])
            feeds_menu.append (feed_mi)
            entries_menu = gtk.Menu ()
            feed_mi.set_submenu (entries_menu)
            i = 0
            for entry in feed_data.entries:
                # We limit the number of entries. Again,
                # this should be configured by the user
                if i >= 10:
                    break
                entry_item = gtk.MenuItem (entry.title)
                entry_item.connect ("activate", feed_activated_cb, entry.link)
                entries_menu.append (entry_item)
                i += 1

        feeds_menu.show_all ()
        old_menu = self.feeds_mi.get_submenu ()
        if old_menu != None:
            old_menu.destroy ()
        self.feeds_mi.set_submenu (feeds_menu)

def feed_activated_cb (item, url):
    exo.url_show (url)

def size_changed_cb (plugin, size, dummy):
    if plugin.get_orientation () == gtk.ORIENTATION_HORIZONTAL:
        plugin.set_size_request (-1, size)
    else:
        plugin.set_size_request (size, -1)

    return True
    
def configure_cb (plugin, dummy):
    dlg = PropertiesDialog (plugin.config)
    dlg.show_all ()

def update_menu_cb (plugin):
    plugin.setup_feeds_menu ()
    return True

def destroy_cb (plugin, dummy):
    gobject.source_remove (plugin.update_id)
