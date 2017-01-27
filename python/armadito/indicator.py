# Copyright (C) 2016 Teclib'

# This file is part of Armadito.

# Armadito indicator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Armadito indicator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Armadito module clamav.  If not, see <http://www.gnu.org/licenses/>.

import os
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GdkPixbuf as gdkpixbuf
import locale
from gettext import gettext as _

APPINDICATOR_ID = 'indicator-armadito'
#IMAGE_FILE = '/home/fdechelle/projects/armadito/git/armadito-gui/web/app/images/armadito-systray.png'
IMAGE_FILE = '/home/fdechelle/Téléchargements/RefonteLogo04-icon.png'

class ArmaditoIndicator(object):
    def __init__(self):
        self.indicator_init(self.build_menu())
        self.notify_init()
        #self.welcome()

    def indicator_init(self, menu):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID,
                                                    os.path.abspath(IMAGE_FILE),
                                                    appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(menu)

    def build_menu(self):
        menu = gtk.Menu()
        menu_item = gtk.CheckMenuItem.new_with_label(_('Real-time protection'))
        menu_item.connect("activate", self.rtprot_menu_activated)
        menu.append(menu_item)
        menu.show_all()        
        return menu

    def notify_init(self):
        notify.init(APPINDICATOR_ID)
        self.notification = notify.Notification.new("Alert!")
        image = gdkpixbuf.Pixbuf.new_from_file(IMAGE_FILE)
        self.notification.set_image_from_pixbuf(image)

    def welcome(self):
        self.messagedialog = gtk.MessageDialog(parent=None, type=gtk.MessageType.WARNING, buttons=gtk.ButtonsType.OK, message_format=_("launching the sausage-rat..."))
        image = gdkpixbuf.Pixbuf.new_from_file(IMAGE_FILE)
        self.messagedialog.set_icon(image)
        self.messagedialog.connect("response", self.welcome_response)
        self.messagedialog.show()

    def rtprot_menu_activated(self, menu_item):
        print("activated %s" % (str(menu_item), ))
        menu_item.toggled()

    def notify(self):
        self.notification.update(_("<b>Yes!</b>"), _("sausage-rat put into orbit successfully!!!"))
        self.notification.show()

    def welcome_response(self, widget, response_id):
        self.notify()
        widget.destroy()
