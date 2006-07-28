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

from ConfigParser import SafeConfigParser

class PluginConfig:
    def __init__ (self, path, new):
        self.path = path
        self.init_defaults ()
        if not new:
            self.read_config ()
        else:
            self.changed = True
            
    def init_defaults (self):
        self.changed = False
        self.params = dict ()
        self.feeds = list ()

    def read_config (self):
        parser = SafeConfigParser ()
        rc = file (self.path, "r")
        parser.readfp (rc)
        rc.close ()

        i = 0
        while parser.has_option ("feeds", "name"+str(i)) and \
              parser.has_option ("feeds", "url"+str(i)):
            self.feeds.append (
                { "name" : parser.get ("feeds", "name"+str(i)),
                  "url"  : parser.get ("feeds", "url"+str(i)) }
                )
            i += 1

    def write_config (self):
        if not self.changed:
            return
        
        parser = SafeConfigParser ()
        parser.add_section ("defaults")
        parser.add_section ("feeds")

        i = 0
        for feed in self.feeds:
            parser.set ("feeds", "name"+str(i), feed["name"])
            parser.set ("feeds", "url"+str(i), feed["url"])
            i += 1

        rc = file (self.path, "w")
        parser.write (rc)
        rc.close ()

        self.changed = False

    def get_param (self, param):
        return self.params[param]

    def set_param (self, param, value):
        self.params[param] = value
        self.changed = True

    def traverse_feeds (self):
        return self.feeds.__iter__ ()

    def clear_feeds (self):
        while len (self.feeds) > 0:
            self.feeds.pop ()
        self.changed = True

    def add_feed (self, name, url):
        self.feeds.append (
            { 'name' : name,
              'url'  : url  }
            )
        self.changed = True

    def feeds_number (self):
        return len (self.feeds)
