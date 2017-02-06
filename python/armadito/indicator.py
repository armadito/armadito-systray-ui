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
from armadito import jrpc
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GdkPixbuf as gdkpixbuf
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
        self.indicator_init()
        self.notify_init()
        self.jrpc = jrpc.Connection('/tmp/.armadito-daemon')
        self.jrpc.set_change_cb(self.on_connection_change)
        self.jrpc.connect()
#    c.map({ 'notify_event' : (lambda o : i.notify(str(o))) })
#c.map({ 'notify_event' : (lambda o : print('lambda %s' % (str(o),))) })
    
        #self.welcome()

    def on_connection_change(self, connected):
        print("connected:", connected)
        if connected:
            self.indicator.set_icon('indicator-armadito-dark')
        else:
            self.indicator.set_icon('indicator-armadito')

    def indicator_init(self):
        self.indicator = appindicator.Indicator.new(INDICATOR_ID,
                                                    'indicator-armadito-dark',
                                                    appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_icon_theme_path("/usr/share/icons")
        self.indicator.set_icon('indicator-armadito')
        self.indicator.set_menu(self.build_menu())

    def build_menu(self):
        menu = gtk.Menu()
        self.version_menu_item = gtk.MenuItem(_('Armadito: version ?.?.?'))
        self.version_menu_item.set_sensitive(False)
        menu.append(self.version_menu_item)
        menu_item = gtk.MenuItem(_('Latest bases update: 01/01/1970 00:00'))
        menu.append(menu_item)
        menu.append(gtk.SeparatorMenuItem())
        menu_item = gtk.MenuItem(_('Open Armadito web interface'))
        menu_item.connect("activate", self.open_web_ui_menu_activated)
        menu.append(menu_item)
        menu_item = gtk.CheckMenuItem.new_with_label(_('Real-time protection'))
        menu_item.connect("activate", self.rtprot_menu_activated)
        menu.append(menu_item)
        menu.append(gtk.SeparatorMenuItem())
        menu.show_all()        
        return menu

    def notify_init(self):
        notify.init(INDICATOR_ID)
        self.notification = notify.Notification.new("Alert!")
#        image = gdkpixbuf.Pixbuf.new_from_file(IMAGE_FILE)
#        self.notification.set_image_from_pixbuf(image)

    def welcome(self):
        self.messagedialog = gtk.MessageDialog(parent=None, type=gtk.MessageType.WARNING, buttons=gtk.ButtonsType.OK, message_format=_("launching the sausage-rat..."))
        image = gdkpixbuf.Pixbuf.new_from_file(IMAGE_FILE)
        self.messagedialog.set_icon(image)
        self.messagedialog.connect("response", self.welcome_response)
        self.messagedialog.show()

    def open_web_ui_menu_activated(self, menu_item):
        print("activated %s" % (str(menu_item), ))

    def rtprot_menu_activated(self, menu_item):
        print("activated %s" % (str(menu_item), ))
        menu_item.toggled()

    def notify(self, msg):
#        self.notification.update(_("<b>Yes!</b>"), _("sausage-rat put into orbit successfully!!!"))
        self.notification.update(_("<b>notify!</b>"), _(msg))
        self.notification.show()

    def welcome_response(self, widget, response_id):
        self.notify()
        widget.destroy()
