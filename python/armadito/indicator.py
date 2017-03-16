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

state2icon = { \
               model.AntivirusState.absent : 'indicator-armadito-desactive.svg', \
               model.AntivirusState.not_working : 'indicator-armadito-desactive.svg', \
               model.AntivirusState.not_up_to_date : 'indicator-armadito-dark.svg', \
               model.AntivirusState.working_and_up_to_date : 'indicator-armadito-dark.svg', \
}

class ArmaditoIndicator(object):
    def __init__(self):
        self._model = model.AntivirusModel()
        self._model.notify_property('state', self._on_state_change)
        self._indicator_init()
        self._notify_init()
        self._model.connect()

    def _on_state_change(self, old_state, state):
        self.indicator.set_icon(state2icon[state])
        
    def _on_status(self, info):
        self._version_menu_item.set_label(_('Armadito: version %s') % (self._model.version,))
        self._update_date = datetime.datetime.fromtimestamp(info.global_update_ts).strftime('%x %X')
        self._update_date_menu_item.set_label(_('Latest bases update: %s') % (self._model.update_date))

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
        self._version_menu_item = gtk.MenuItem(_('Armadito: version %s') % (self._model.version,))
        self._version_menu_item.set_sensitive(False)
        menu.append(self._version_menu_item)
        self._update_date_menu_item = gtk.MenuItem(_('Latest bases update: %s') % (self._model.update_date))
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

