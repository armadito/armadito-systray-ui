# Copyright (C) 2016-2017 Teclib'

# This file is part of Armadito indicator.

# Armadito indicator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Armadito indicator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Armadito indicator.  If not, see <http://www.gnu.org/licenses/>.

import os
from armadito import jrpc, model
from gi.repository import Gtk as gtk
from gi.repository import Gio as gio
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GdkPixbuf as gdkpixbuf
from gi.repository import GObject as gobject
import datetime
import locale
from gettext import gettext as _

INDICATOR_ID='indicator-armadito'

# menu entries:
# Armadito version x.y.z
# Latest bases update: 01/01/1970 00:00
# separator
# Open Armadito web interface
# Pause real-time protection
# separator
# Latest threats ???

class ArmaditoIndicator(object):
    def __init__(self):
        self._antivirus_version = _('<unknown>')
        self._update_date = _('<unknown>')
        self._indicator_init()
        self._notify_init()
        self._connection_init()
        if self._connected:
            self._conn.call("status", callback = self._on_status)

    def _on_status(self, info):
        self._antivirus_version = info.antivirus_version
        self._version_menu_item.set_label(_('Armadito: version %s') % (self._antivirus_version,))
        self._update_date = datetime.datetime.fromtimestamp(info.global_update_ts).strftime('%x %X')
        self._update_date_menu_item.set_label(_('Latest bases update: %s') % (self._update_date))

    def _on_timeout(self):
        try:
            self._conn.connect()
        except OSError as e:
            print(str(e))
            return True
        self._timeout_id = None
        return False

    def _start_timeout(self):
            self._timeout_id = gobject.timeout_add(1000, self._on_timeout)

    def _connection_listener(self, connected):
        print("connected:", connected)
        if connected:
            self.indicator.set_icon('indicator-armadito-dark')
        else:
            self.indicator.set_icon('indicator-armadito-missing')
            if self._connected is True:
                self._start_timeout()
        self._connected = connected
        
    def _connection_init(self):
        self._connected = False
        self._conn = jrpc.Connection('\0/tmp/.armadito-daemon')
        #    c.map({ 'notify_event' : (lambda o : i.notify(str(o))) })
        #c.map({ 'notify_event' : (lambda o : print('lambda %s' % (str(o),))) })
        self._timeout_id = None
        self._conn.set_listener(self._connection_listener)
        try:
            self._conn.connect()
        except OSError as e:
            print(str(e))
            self._start_timeout()

    def _indicator_init(self):
        self.indicator = appindicator.Indicator.new(INDICATOR_ID,
                                                    'indicator-armadito-dark',
                                                    appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_icon_theme_path("/usr/share/icons")
        self.indicator.set_icon('indicator-armadito')
        self.indicator.set_menu(self._build_menu_gtk())

    def _build_menu_gtk(self):
        menu = gtk.Menu()
        self._version_menu_item = gtk.MenuItem(_('Armadito: version %s') % (self._antivirus_version,))
        self._version_menu_item.set_sensitive(False)
        menu.append(self._version_menu_item)
        self._update_date_menu_item = gtk.MenuItem(_('Latest bases update: %s') % (self._update_date))
        self._update_date_menu_item.set_sensitive(False)
        menu.append(self._update_date_menu_item)
        menu.append(gtk.SeparatorMenuItem())
        menu_item = gtk.CheckMenuItem.new_with_label(_('Real-time protection'))
        menu_item.connect("activate", self._rtprot_menu_activated)
        menu.append(menu_item)
        #menu.append(gtk.SeparatorMenuItem())
        #menu_item = self._build_animated_menu_item()
        #print(menu_item)
        #menu.append(menu_item)
        menu.show_all()        
        return menu

    # trial, does not work
    def _build_animated_menu_item(self):
        box = gtk.Box(gtk.Orientation.HORIZONTAL, 6)
        #icon = gtk.Image.new_from_file('...')
        # works only if you do:
        #gsettings set org.gnome.desktop.interface menus-have-icons true
        icon = gtk.Image.new_from_icon_name("folder-music-symbolic", gtk.IconSize.MENU)
        print(icon)
        label = gtk.Label('animated')
        menu_item = gtk.MenuItem()
        box.add(icon)
        box.add(label)
        menu_item.add(box)
        menu_item.show_all()
        return menu_item

    def _build_menu_gio(self):
        menu = gio.Menu()
        section = gio.Menu()
        section.append_item(gio.MenuItem.new(_('Armadito: version %s') % (self._antivirus_version,), None))
        menu.append_section("foobar", section)
        return menu
        
    # trial, does not work
    def _notify_init(self):
        notify.init(INDICATOR_ID)
        self._notification = notify.Notification.new("Alert!")
#        image = gdkpixbuf.Pixbuf.new_from_file(IMAGE_FILE)
#        self.notification.set_image_from_pixbuf(image)

    def _rtprot_menu_activated(self, menu_item):
        print("activated %s" % (str(menu_item), ))
        menu_item.toggled()

    def notify(self, msg):
        self.notification.update(_("<b>notify!</b>"), _(msg))
        self.notification.show()

