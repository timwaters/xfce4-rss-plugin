#!/usr/bin/python
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
import sys

from xfce4.rssplugin.plugin import RSSPlugin

plugin = RSSPlugin ()
plugin.show ()
gtk.main ()
sys.exit (0)
