#!-*- coding:utf-8 -*-
from gi.repository import GLib
import threading
from Xlib import display,X
from Xlib.ext import record
from Xlib.protocol import rq
import threading
import os
#display.Display()
#local_dpy =display.Display()
#record_dpy = display.Display()
#CTX = None
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
            print('Error: RECORD extension not found!')
            return False
        self.record_dpy.record_enable_context(self.ctx, record_callback)
        print "free"
        self.record_dpy.record_free_context(self.ctx)

    def get_event_data(self,data):
        return rq.EventField(None).parse_binary_value(data, self.record_dpy.display, None, None)



    def check_valid_event(self,reply):
        if reply.category != record.FromServer:
            return 
        if reply.client_swapped:
            return
        if not len(reply.data) or ord(reply.data[0]) < 2:
            return



    def record_callback(self,reply):
        self.check_valid_event(reply)
     
        data = reply.data
        while len(data):
            event, data = self.get_event_data(data)
            #self.capture_event.emit(event)
            if event.type == X.ButtonRelease:
                print self.clip
                #GLib.idle_add(self.clip._on_owner_change)
                GLib.idle_add(self.clip.emit,"need_clip")
                #text = self.clip.primary.wait_for_text() #os.system("xclip -o")
                #if text != None:
                    #print text
                #else:
                    #print("No text on the clipboard.")
                    #return False
            elif event.type == X.MotionNotify:
                pass
                #print "x=%d,y=%d" % (event.root_x,event.root_y)
            #elif event.type == X.DestroyNotify:
                #print "close"
                #r=record_dpy.record_disable_context(CTX)
                #record_dpy.flush()
                #print r
                #return


    def run(self):
        print "work run"
        self.record_event(self.record_callback)

#def record_thread_start(clip):
    #t=threading.Thread(target=record_worker,args=[clip])
    ##t.setDaemon(True)
    #t.start()
    def stop(self):
        print "enddddddddd"
        self.local_dpy.record_disable_context(self.ctx)
        self.local_dpy.flush()
        #return
