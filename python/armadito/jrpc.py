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
# * implement mapper
# * implement notification handling
# * implement method call with id

class MarshallingError(Exception):
    """Marshalling exception for marshall() and unmarshall() functions"""
    pass

class MarshallObject(object):
    pass

def unmarshall(j_obj):
    tj = type(j_obj)
    if t_obu is str or tj is int:
        return j_obj
    elif tj is dict:
        o = MarshallObject()
        for k, v in j_obj.items():
            setattr(o, k, unmarshall(v))
        return o
    elif tj is list:
        l = []
        for i in j_obj:
            l.append(unmarshall(i))
        return l
    raise MarshallingError("invalid type: %s in JSON unmarshalling" % (str(tj))) 

def marshall(obj):
    t = type(obj)
    if t is str or t is int:
        return obj
    elif t is list:
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
    raise MarshallingError("invalid type: %s in JSON marshalling" % (str(t))) 


class JsonRPCError(Exception):
    """JSON-RPC exception"""
    pass

def on_message_received(source, cb_condition, conn):
    if cb_condition & gobject.IO_ERR:
        conn.on_error()
    else:
        conn.on_data()
    return True

class Connection(object):
    def __init__(self, sock_path):
        self.sock = None
        self.sock_path = sock_path
        self.connected = False
        self.change_cb = None
        self.watch_id = None
        self.timeout_id = None
        self.response_callbacks = {}
        self.mapper = {}

    def set_change_cb(self, cb):
        self.change_cb = cb

    def map(self, method, fun):
        self.mapper[method] = fun

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
            self.sock.settimeout(10)
            self.sock.connect(self.sock_path)
        except OSError as e:
            print(str(e))
            self.sock = None
            self.on_error()
            return
        self.watch_id = gobject.io_add_watch(self.sock.fileno(), gobject.IO_IN | gobject.IO_ERR, on_message_received, self)
        if self.connected is False:
            self.connected = True
            if self.change_cb is not None:
                self.change_cb(self.connected)

    def on_error(self):
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

    def on_data(self):
        buff = self.sock.recv(4096)
        j_buff = buff.decode('utf-8')
        if len(j_buff) == 0:
            self.on_error()
            return
        self.dispatch(json.loads(j_buff))
        
    @staticmethod
    def basic_check(jrpc_obj):
        if not 'jsonrpc' in jrpc_obj:
            raise JsonRPCError('missing jsonrpc') 
        if jrpc_obj['jsonrpc'] != '2.0':
            raise JsonRPCError('invalid jsonrpc version') 

    @staticmethod
    def is_request(jrpc_obj):
        return 'method' in jrpc_obj and type(jrpc_obj['method']) is str

    @staticmethod
    def is_response(jrpc_obj):
        return 'result' in jrpc_obj and 'id' in jrpc_obj and 'error' not in jrpc_obj

    def process_request(self, jrpc_obj):
        fun = self.mapper[jrpc_obj['method']]
        if fun is None:
            raise JsonRPCError('unknown method') 
        try:
            params = None
            if 'params' in jrpc_obj:
                params = unmarshall(jrpc_obj['params'])
            fun(params)
        except Exception as e:
            raise JsonRPCError('method call failed', e)

    def process_response(self, jrpc_obj):
        try:
            id = jrpc_obj['id']
            cb = self.response_callbacks[id]
            result = unmarshall(jrpc_obj['result'])
            cb(result)
            del self.response_callbacks[id]
        except KeyError as e:
            raise e

    def dispatch(self, jrpc_obj):
        basic_check(jrpc_obj)
        if is_request(jrpc_obj):
            self.process_request(jrpc_obj)
        elif is_response(jrpc_obj):
            self.process_response(jrpc_obj)

#    def scan(self):
#        p = {'root_path':'/home/fdechelle/Bureau/MalwareStore/EICAR/','send_progress':1}
#        d = {'id':1,'params':p,'jsonrpc':'2.0','method':'scan'}
#        buff = json.dumps(d).encode('utf-8')
#        self.sock.send(buff)
