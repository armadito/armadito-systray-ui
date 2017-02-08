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

class MarshallingError(Exception):
    """Marshalling exception for marshall() and unmarshall() functions"""
    pass

class MarshallObject(object):
    pass

def unmarshall(j_val):
    """Unmarshall a JSON value into a python value

    Argument: a JSON value (usually returned by json.loads())
    Returns: a python value

    Correspondances between JSON values and python types:
    dict -> object
    list -> list
    int  -> int
    str  -> str
    """
    t = type(j_val)
    if t is str or t is int:
        return j_val
    elif t is dict:
        o = MarshallObject()
        for k, v in j_val.items():
            setattr(o, k, unmarshall(v))
        return o
    elif t is list:
        l = []
        for item in j_val:
            l.append(unmarshall(item))
        return l
    raise MarshallingError("invalid type: %s in JSON unmarshalling" % (str(t))) 

def marshall(val):
    """Marshall a python object into a JSON value

    Argument: a python value
    Returns: a JSON value that can be passed to json.dumps())

    Correspondances between JSON values and python types:
    object ->  dict
    list   -> list
    int    -> int
    str    -> str
    """
    t = type(val)
    if t is str or t is int:
        return val
    elif t is list:
        l = []
        for i in val:
            l.append(marshall(i))
        return l
    elif isinstance(val, object):
        d = {}
        for attr in dir(val):
            if not '__' in attr:
                d[attr] = marshall(getattr(val, attr))
        return d
    raise MarshallingError("invalid type: %s in JSON marshalling" % (str(t))) 

class JsonRPCError(Exception):
    """JSON-RPC exception"""
    pass

def _on_message_received(source, cb_condition, conn):
    if cb_condition & gobject.IO_ERR:
        return conn._on_error()
    elif cb_condition & gobject.IO_IN:
        return conn._on_data()
    return False

def _basic_check(jrpc_obj):
    if not 'jsonrpc' in jrpc_obj:
        raise JsonRPCError('missing jsonrpc') 
    if jrpc_obj['jsonrpc'] != '2.0':
        raise JsonRPCError('invalid jsonrpc version') 

def _is_request(jrpc_obj):
    return 'method' in jrpc_obj and type(jrpc_obj['method']) is str

def _is_response(jrpc_obj):
    return 'result' in jrpc_obj and 'id' in jrpc_obj and not 'error' in jrpc_obj

class Connection(object):
    """JSON-RPC connection over a Unix socket

    Provides methods and notifications calls, and asynchronous callbacks.
    Provides incoming calls processing (only notifications for now)
    """
    def __init__(self, sock_path):
        """Arguments:
        sock_path -- the path to the Unix socket
        """
        self._sock = None
        self._sock_path = sock_path
        self._watch_id = None
        self._connection_listeners = []
        self._response_id = 1
        self._response_callbacks = {}
        self._mapper = {}

    def map(self, method, fun):
        """maps incoming calls
        Arguments:
        method -- the 'method' in JSON-RPC request
        fun    -- the callable to call when receiving a JSON-RPC request
        """
        self._mapper[method] = fun

    def add_listener(self, listener):
        self._connection_listeners.append(listener)

    def remove_listener(self, listener):
        self._connection_listeners.remove(listener)

    def _notify_listeners(self, connected):
        for listener in self._connection_listeners:
            listener(connected)

    def connect(self):
        """connects to Unix socket and install file descriptor watch callback"""
        try:
            self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
            self._sock.settimeout(10)
            self._sock.connect(self._sock_path)
        except OSError:
            self._sock = None
            raise
        self._watch_id = gobject.io_add_watch(self._sock.fileno(), gobject.IO_IN | gobject.IO_ERR, _on_message_received, self)
        self._notify_listeners(True)

    def _close(self):
        self._sock.close()
        self._sock = None
        self._notify_listeners(False)
        self._watch_id = None
        
    def close(self):
        """close the Unix socket and remove file descriptor watch callback"""
        gobject.source_remove(self._watch_id)
        self._close()

    def _on_error(self):
        if self._sock is not None:
            self._close()
        return False

    def _on_data(self):
        buff = self._sock.recv(4096)
        j_buff = buff.decode('utf-8')
        if len(j_buff) == 0:
            self._close()
            return False
        self._dispatch(json.loads(j_buff))
        return True
        
    def _process_request(self, jrpc_obj):
        method = jrpc_obj['method']
        if not method in self._mapper:
            raise JsonRPCError('no callable for method %s' % (method,))
        fun = self._mapper[method]
        params = None
        if 'params' in jrpc_obj:
            params = unmarshall(jrpc_obj['params'])
            fun(params)
        else:
            fun()

    def _process_response(self, jrpc_obj):
        id = jrpc_obj['id']
        if not id in self._response_callbacks:
            raise JsonRPCError('no callback for id %d' % (id,))
        cb = self._response_callbacks[id]
        del self._response_callbacks[id]
        result = unmarshall(jrpc_obj['result'])
        cb(result)

    def _dispatch(self, jrpc_obj):
        _basic_check(jrpc_obj)
        if _is_request(jrpc_obj):
            self._process_request(jrpc_obj)
        elif _is_response(jrpc_obj):
            self._process_response(jrpc_obj)
        else:
            raise JsonRPCError('not implemented JSON-RPC: %s' % (repr(jrpc_obj)))

    def _new_id(self):
        id = self._response_id
        self._response_id += 1
        return id

    def call(self, method, params = None, callback = None):
        """Do a JSON-RPC call

        Arguments:
        method    -- the 'method' in JSON-RPC request
        params    -- an object to be marshalled into JSON and passed as 'params' in JSON-RPC request
        callback  -- a callable that will be called when receiving the JSON-RPC response
        """
        jrpc_obj = {'jsonrpc':'2.0', 'method':method}
        if params is not None:
            j_params = marshall(params)
            jrpc_obj['params'] = j_params
        if callback is not None:
            id = self._new_id()
            jrpc_obj['id'] = id
            self._response_callbacks[id] = callback
        buff = json.dumps(jrpc_obj).encode('utf-8')
        self._sock.send(buff, socket.MSG_EOR)

    def notify(self, method, params = None):
        """Do a JSON-RPC notify (call without 'id', therefore without returned result)"""
        self.call(method)
