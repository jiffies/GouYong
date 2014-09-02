#-*- coding:utf-8 -*-
from gi.repository import Gdk,Gtk,GLib,WebKit,GObject
import urllib2
import youdaoQuery
import os
import sys
import record
import os.path
from dict_manager import DictManager
import utils
WIDTH = 800
HEIGHT = 280
MOUSE_DETECT_INTERVAL = 100
LEAVE_BORDER_WIDTH = 50

class Popup(object):
    def __init__(self):
        self.popup=Gtk.Window.new(Gtk.WindowType.POPUP)
        self.popup.set_default_size(WIDTH, HEIGHT)
        self.hbox = Gtk.Box(spacing=0)
        self.popup.add(self.hbox)
        self.web = WebKit.WebView.new()
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.add(self.web)
        self.hbox.add(self.scroll)
        self.label = Gtk.Label()
        self.hbox.pack_start(self.label,True,True,0)
        self.gravity=None
    
    def load_uri(self,url):
        print url
        self.web.load_uri(url)
    
    def reload(self):
        self.web.reload()
    

class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.display = self.get_display()
        self.screen = self.get_screen()
        self.screen_width = self.screen.width()
        self.screen_height = self.screen.height()
        self.connect("delete-event", self._on_delete_event)
        self.iconify()
        self.show_all()
        self.dir=os.getcwd()
    def _on_delete_event(self,*args):
        self.rc.stop()
        Gtk.main_quit()
        
class Clip(GObject.GObject):
    __gsignals__ = {
            "need_clip":(GObject.SIGNAL_RUN_FIRST,None,())
            }
    
    def do_need_clip(self):
        print "need"
        self._on_owner_change()

    def __init__(self,main_win,popup,dm):
        super(Clip,self).__init__()
        self.main_win = main_win
        self.popup = popup
        #dict manager
        self.dm = dm
        self.isNet = True
        self.primary=Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        #self.primary.connect('owner-change',self._on_owner_change)
        

    def _is_out(self,x,y,center_pointer,width,height):
        gravity = self.popup.gravity
        lbw=LEAVE_BORDER_WIDTH
        if gravity == Gdk.Gravity.NORTH_WEST:
            if center_pointer['x']-lbw <x<(center_pointer['x']+width+lbw) and center_pointer['y']-lbw <y<(center_pointer['y']+height+lbw):
                return False
        elif gravity==Gdk.Gravity.SOUTH_WEST:
            if center_pointer['x']-lbw <x<(center_pointer['x']+width+lbw) and (center_pointer['y']-height-lbw) <y<(center_pointer['y']+lbw):
                return False

        elif gravity==Gdk.Gravity.NORTH_EAST:
            if (center_pointer['x']-width-lbw) <x<(center_pointer['x']+lbw) and center_pointer['y']-lbw <y<(center_pointer['y']+height+lbw):
                return False

        elif gravity==Gdk.Gravity.SOUTH_EAST:
            if (center_pointer['x']-width-lbw) <x<(center_pointer['x']+lbw) and (center_pointer['y']-height-lbw) <y<(center_pointer['y']+lbw):
                return False
        if (x-center_pointer['x'])**2+(y-center_pointer['y'])**2>lbw*lbw:
            return True 
        else:
            return False

    def _check_mouse(self,center):
        s,x,y,m=self.main_win.display.get_pointer()
        print "x= %f,y=%f" % (x,y)
        if self._is_out(x,y,center,WIDTH,HEIGHT):
            self.popup.popup.hide()
            return False
        else:
            return True

    def _placement(self,click_x,click_y):
        place_x=None
        place_y=None
        gravity=None
        w,h=self.popup.popup.get_size()
        if self.main_win.screen_width-click_x > w:
            if self.main_win.screen_height-click_y > h:
                gravity=Gdk.Gravity.NORTH_WEST
                place_x=click_x
                place_y=click_y
            else:
                gravity=Gdk.Gravity.SOUTH_WEST
                place_x=click_x
                place_y=click_y-h
        else:
            if self.main_win.screen_height-click_y > h:
                gravity=Gdk.Gravity.NORTH_EAST
                place_x=click_x-w
                place_y=click_y
            else:
                gravity=Gdk.Gravity.SOUTH_EAST
                place_x=click_x-w
                place_y=click_y-h
        self.popup.popup.set_gravity(gravity)
        self.popup.gravity = gravity
        self.popup.popup.move(place_x,place_y)

    def _on_owner_change(self):
        text = self.primary.wait_for_text()
        if text:
            print text
        else:
            print("No text on the clipboard.")
            return False
        self.primary.set_text('',0)
        s,x,y,m=self.main_win.display.get_pointer()
        print "x= %f,y=%f" % (x,y)
        if self.isNet:
            try:
                results=youdaoQuery.gettext(text)
                fileName=youdaoQuery.creat_file(text,results)
                uri = 'file://'+os.path.join(self.main_win.dir,fileName)
                self.popup.load_uri(uri)
            except urllib2.URLError:
                print "You are disconnected."
                self.isNet = False
        else:
            text=utils.tidy_text(text)
            results=self.dm.dict[text]
            print results
            self.popup.label.set_text(results)

        self._placement(x,y)
        self.popup.popup.show_all()
        center={'x':x,'y':y}
        Gdk.threads_add_timeout(GLib.PRIORITY_DEFAULT_IDLE,MOUSE_DETECT_INTERVAL,self._check_mouse,center)




def main():
    pop=Popup()
    win=MainWindow()
    dm = DictManager()
    dm.open_dict()
    clip=Clip(win,pop,dm)
    #record client thread start
    rc=record.RecordClient(clip)
    win.rc = rc
    rc.start()
    Gtk.main()

if __name__ == "__main__":
    main()
