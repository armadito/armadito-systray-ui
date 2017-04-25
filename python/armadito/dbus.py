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

import dbus
import dbus.service

class AntivirusObject(dbus.service.Object):
    def __init__(self, antivirus):
        session_bus = dbus.SessionBus()
        name = dbus.service.BusName("org.armadito.AntivirusService", session_bus)
        super().__init__(name, '/')
        self._antivirus = antivirus

    @dbus.service.method("org.armadito.AntivirusInterface",
                         in_signature='s', out_signature='')
    def scan(self, path):
        print('org.armadito.AntivirusInterface.scan(%s)' % (str(path),))
        self._antivirus.scan(str(path))
