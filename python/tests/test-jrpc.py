#!/usr/bin/python3

from gi.repository import Gtk as gtk
from armadito import jrpc
import pprint
import sys

conn = jrpc.Connection('/tmp/.armadito-daemon')
conn.connect()

def on_status_received(result): 
    pprint.pprint(vars(result))
    pprint.pprint(vars(result.module_infos[0]))
    for b in result.module_infos[0].base_infos:
        pprint.pprint(vars(b))
    #sys.exit(0)
    
conn.call('status', callback = on_status_received)

def notify_event(ev):
    pprint.pprint(vars(ev))
    pprint.pprint(vars(ev.u))
    if ev.type == 'EVENT_DETECTION':
        pprint.pprint(vars(ev.u.ev_detection))

conn.map('notify_event', notify_event)

class ScanArgument(object):
    def __init__(self, path):
        self.root_path = path
        self.send_progress = 1

conn.call('scan', ScanArgument(sys.argv[1]))

gtk.main()
