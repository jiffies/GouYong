#!-*- coding:utf-8 -*-
from gi.repository import GLib
import threading
from Xlib import display, X, XK
from Xlib.ext import record
from Xlib.protocol import rq
import threading
import os
from GouYong.src import log
# from GouYong.src. import log
logger = log.get_logger(__name__)


class RecordClient(threading.Thread):
    def __init__(self,clip):
        super(RecordClient,self).__init__()
        self.ctx = None
        self.clip = clip
        self.event = []
        self.local_dpy = display.Display()
        self.record_dpy = display.Display()

    def record_event(self,record_callback):
        self.ctx = self.record_dpy.record_create_context(
            0,
            [record.AllClients],
            [{
                    'core_requests': (0, 0),
                    'core_replies': (0, 0),
                    'ext_requests': (0, 0, 0, 0),
                    'ext_replies': (0, 0, 0, 0),
                    'delivered_events': (0, 0),
                    'device_events': (X.KeyPress, X.MotionNotify),
                    'errors': (0, 0),
                    'client_started': False,
                    'client_died': False,
                    }])


        if not self.record_dpy.has_extension('RECORD'):
            logger.critical('Error: RECORD extension not found!')
            return False
        self.record_dpy.record_enable_context(self.ctx, record_callback)
        logger.debug("free")
        self.record_dpy.record_free_context(self.ctx)

    def check_valid_event(self,reply):
        if reply.category != record.FromServer:
            return True
        if reply.client_swapped:
            return True
        if not len(reply.data) or (reply.data[0] < 2):
            return True

    def lookup_keysym(self, keysym):
        for name in dir(XK):
            if name[:3] == "XK_" and getattr(XK, name) == keysym:
                return name[3:]
        return "[%d]" % keysym

    def record_callback(self,reply):
        if self.check_valid_event(reply):
            return

        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, self.record_dpy.display, None, None)
            if event.type == X.KeyRelease:
                keysym = self.local_dpy.keycode_to_keysym(event.detail, 0)
                if not keysym:
                    print("KeyCode", event.detail)
                    self.event.clear()
                key = self.lookup_keysym(keysym)
                event.keystr = key
                if key in ['Control_L', 'Control_R']:
                    self.event.append(event)
                else:
                    self.event.clear()
            elif event.type == X.KeyPress:
                pass
            else:
                self.event.clear()

        if len(self.event) == 2:
            if (self.event[1].time - self.event[0].time) > 400:
                self.event.clear()
                return
            if self.event[0].keystr == self.event[1].keystr == 'Control_L':
                GLib.timeout_add(0,self.clip.emit,"need_clip",event.time)
            if self.event[0].keystr == self.event[1].keystr == 'Control_R':
                self.clip.change_cht_state(True)
                GLib.timeout_add(0,self.clip.emit,"need_clip",event.time)
            self.event.clear()

    def run(self):
        logger.debug("work run")
        self.record_event(self.record_callback)

    def stop(self):
        logger.debug("enddddddddd")
        self.local_dpy.record_disable_context(self.ctx)
        self.local_dpy.flush()
