#!-*- coding:utf-8 -*-
from gi.repository import GLib
import threading
from Xlib import display,X
from Xlib.ext import record
from Xlib.protocol import rq
import threading
import os
import log
logger = log.get_logger(__name__)

class RecordClient(threading.Thread):
    def __init__(self,clip):
        super(RecordClient,self).__init__()
        self.ctx = None
        self.clip = clip
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

    def get_event_data(self,data):
        return rq.EventField(None).parse_binary_value(data, self.record_dpy.display, None, None)



    def check_valid_event(self,reply):
        if reply.category != record.FromServer:
            return True
        if reply.client_swapped:
            return True
        if not len(reply.data) or (reply.data[0] < 2):
            return True

    def record_callback(self,reply):
        if self.check_valid_event(reply):
            return

        data = reply.data
        while len(data):
            event, data = self.get_event_data(data)
            if event.type == X.ButtonRelease:
                if event.state & X.Button1Mask:
                    #GLib.idle_add(self.clip.emit,"need_clip",event.time)
                    #ButtonRelease事件比SelectionClear事件早发送，所以等待10ms再取词，让取词在_on_owner_change回调之后执行,emit return None
                    GLib.timeout_add(10,self.clip.emit,"need_clip",event.time)
            elif event.type == X.MotionNotify:
                pass


    def run(self):
        logger.debug("work run")
        self.record_event(self.record_callback)

    def stop(self):
        logger.debug("enddddddddd")
        self.local_dpy.record_disable_context(self.ctx)
        self.local_dpy.flush()
