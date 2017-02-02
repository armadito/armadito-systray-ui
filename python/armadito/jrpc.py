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
from gi.repository import GObject as gobject

# TODO
# * close socket and remove watch on error
# * implement mapper
# * implement notification handling

def on_message_received(source, cb_condition, conn):
    if cb_condition & gobject.IO_ERR:
        conn.process_error()
    else:
        conn.process_data()
    return True

class MarshallObject(object):
    pass

def unmarshall(j_obj):
    if type(j_obj) is str or type(j_obj) is int:
        return j_obj
    elif type(j_obj) is dict:
        o = MarshallObject()
        for k, v in j_obj.items():
            setattr(o, k, unmarshall(v))
        return o
    elif type(j_obj) is list:
        l = []
        for i in j_obj:
            l.append(unmarshall(i))
        return l

def marshall(obj):
    if type(obj) is str or type(obj) is int:
        return obj
    elif type(obj) is list:
        l = []
        for i in obj:
            l.append(marshall(i))
        return l
    elif isinstance(obj, object):
        d = {}
        for a in dir(obj):
            if not '__' in a:
                d[a] = marshall(getattr(obj, a))
        return d

class Connection(object):
    def __init__(self, sock_path):
        self.sock = None
        self.sock_path = sock_path
        self.connected = False
        self.change_cb = None
        self.watch_id = None
        self.timeout_id = None

    def add_change_cb(self, cb):
        self.change_cb = cb

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
            self.sock.settimeout(10)
            self.sock.connect(self.sock_path)
        except OSError as e:
            print(str(e))
            self.sock = None
            self.process_error()
            return
        self.watch_id = gobject.io_add_watch(self.sock.fileno(), gobject.IO_IN | gobject.IO_ERR, on_message_received, self)
        if self.connected is False:
            self.connected = True
            if self.change_cb is not None:
                self.change_cb(self.connected)

    def process_error(self):
        if self.connected:
            self.sock.close()
            self.sock = None
            self.connected = False
            self.watch_id = None
            if self.change_cb is not None:
                self.change_cb(self.connected)
        if self.timeout_id is None:
            self.timeout_id = gobject.timeout_add(1000, self.on_timeout)

    def on_timeout(self):
        self.connect()
        if self.connected:
            self.timeout_id = None
            return False
        return True

    def process_data(self):
        buff = self.sock.recv(4096)
        j_buff = buff.decode('utf-8')
        if len(j_buff) == 0:
            self.process_error()
            return
        d = json.loads(j_buff)
        jrpc_obj = unmarshall(d)
        self.dispatch(jrpc_obj)
        
    def map(self, m):
        self.mapper = m

    def dispatch_request(self, jrpc_obj):
        fun = self.mapper[jrpc_obj.method]
        if fun is not None:
            fun(jrpc_obj.params)

    def dispatch(self, jrpc_obj):
        if is_request(jrpc_obj):
            dispatch_request(jrpc_obj)

    def scan(self):
        p = {'root_path':'/home/fdechelle/Bureau/MalwareStore/EICAR/','send_progress':1}
        d = {'id':1,'params':p,'jsonrpc':'2.0','method':'scan'}
        buff = json.dumps(d).encode('utf-8')
        self.sock.send(buff)
