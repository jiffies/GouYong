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
from indicator import DictIndicator
import cairo
WIDTH = 700
HEIGHT = 280
OFFLINEWIDTH = 300
OFFLINEHEIGHT = 200
MOUSE_DETECT_INTERVAL = 100
LEAVE_BORDER_WIDTH = 50

class Popup(object):
    def __init__(self):
        self.popup=Gtk.Window.new(Gtk.WindowType.POPUP)
        self.web = WebKit.WebView.new()
        self.label = Gtk.Label()
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.add(self.web)
        self.popup.add(self.scroll)
        self.gravity=None
        self.init_textview()
        self.init_ui()

    def init_textview(self):
        self.textbuffer = Gtk.TextBuffer.new()
        self.textview = Gtk.TextView.new_with_buffer(self.textbuffer)
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        #self.textview.set_opacity(0.5)
   
    def init_ui(self):
        self.popup.set_default_size(WIDTH, HEIGHT)
        self.textview.set_app_paintable(True)
        if self.popup.get_screen().is_composited():
            pass
            #self.popup.set_opacity(0.8)
        else:
            print "Your desktop doesn't support composited."
        self.textview.connect("draw",self._on_draw)
    

    def _on_draw(self,widget,ctx):
        w,h = self.popup.get_size()
        lg = cairo.LinearGradient(0,0,0,h)
        r,g,b=utils.rgb_trans(230, 243, 255)
        lg.add_color_stop_rgba(0,r,g,b,1)
        lg.add_color_stop_rgba(1,1,1,1,1)
        ctx.rectangle(0,0,w,h)
        ctx.set_source(lg)
        ctx.fill()
        return False

    def change_ui_by_net(self,isNet):
        child = self.scroll.get_children()
        if isNet:
            self.scroll.remove(child[0])
            self.scroll.add(self.web)
            self.popup.resize(WIDTH,HEIGHT)
        else:
            self.scroll.remove(child[0])
            self.scroll.add(self.textview)
            self.popup.resize(OFFLINEWIDTH,OFFLINEHEIGHT)

    
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
        with utils.Timer(True) as t:
            self._on_owner_change()

    def __init__(self,main_win,popup,dm):
        super(Clip,self).__init__()
        self.main_win = main_win
        self.popup = popup
        #dict manager
        self.dm = dm
        self.check_mouse_thread_id = None
        self.isNet = True
        self.primary=Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        

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
        #print "id:%d, x= %f,y=%f" % (self.check_mouse_thread_id,x,y)
        w,h = self.popup.popup.get_size()
        if self._is_out(x,y,center,w,h):
            self.popup.popup.hide()
            print "hide============="
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
    
    def change_net_state(self,state):
        self.isNet = state
        self.popup.change_ui_by_net(self.isNet)

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
                self.dictind.toggled(self.dictind.use_web_item,isNet=False)
                return
        else:
            text=utils.tidy_text(text)
            results=self.dm.dict[text]
            print results
            self.popup.textbuffer.set_text(results,len(results))

        self._placement(x,y)
        if self.check_mouse_thread_id and GLib.source_remove(self.check_mouse_thread_id):
            print "check mouse not finish.now kill it."
            #self.popup.popup.hide()
        else:
            print "There is no check mouse thread."
        self.popup.popup.show_all()
        print "show==================="
        center={'x':x,'y':y}
        self.check_mouse_thread_id=Gdk.threads_add_timeout(GLib.PRIORITY_DEFAULT_IDLE,MOUSE_DETECT_INTERVAL,self._check_mouse,center)




def main():
    pop=Popup()
    win=MainWindow()
    dm = DictManager()
    dm.open_dict()
    clip=Clip(win,pop,dm)
    #record client thread start
    ind = DictIndicator(win,clip)
    clip.dictind = ind
    rc=record.RecordClient(clip)
    win.rc = rc
    rc.start()
    Gtk.main()

if __name__ == "__main__":
    main()
