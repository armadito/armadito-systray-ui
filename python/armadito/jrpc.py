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

import json
import socket
import gobject
from gi.repository import GObject as gobject

def on_message_received(source, cb_condition, conn):
    buff = conn.sock.recv(4096)
    print(buff)
    return True

class Connection(object):
    def __init__(self, sock_path):
        self.sock_path = sock_path
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
        self.sock.settimeout(10)

    def connect(self):
        try:
            self.sock.connect(self.sock_path)
        except socket.timeout as e:
            print(str(e))
            pass
        gobject.io_add_watch(self.sock.fileno(), gobject.IO_IN, on_message_received, self)
    
