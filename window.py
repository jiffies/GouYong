#-*- coding:utf-8 -*-
from gi.repository import Gdk,Gtk,GLib,WebKit
import youdaoQuery
WIDTH = 800
HEIGHT = 280
MOUSE_DETECT_INTERVAL = 100

class Popup(object):
    def __init__(self):
        self.popup=Gtk.Window.new(Gtk.WindowType.POPUP)
        self.popup.set_default_size(WIDTH, HEIGHT)
        self.web = WebKit.WebView.new()
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.add(self.web)
        self.popup.add(self.scroll)
        #event
    
    def load_uri(self,url):
        print url
        self.web.load_uri(url)
    
    def reload(self):
        self.web.reload()
    
    #def start(self):
        #self.show_all()
        #Gtk.main()

class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.display = self.get_display()
        self.screen = self.get_screen()
        self.connect("delete-event", Gtk.main_quit)
        self.iconify()
        self.show_all()
        
class Clip(object):
    def __init__(self,main_win,popup):
        self.main_win = main_win
        self.popup = popup
        self.primary=Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        self.primary.connect('owner-change',self._on_owner_change)
        

    def _is_out(self,x,y,center_pointer,width,height):
        if x>center_pointer['x']-50 and x<(center_pointer['x']+width+50) and y>center_pointer['y']-50 and y<(center_pointer['y']+height+50):
            return False
        elif (x-center_pointer['x'])**2+(y-center_pointer['y'])**2>50*50:
            return True 

    def _check_mouse(self,center):
        s,x,y,m=self.main_win.display.get_pointer()
        print "x= %f,y=%f" % (x,y)
        if self._is_out(x,y,center,WIDTH,HEIGHT):
            self.popup.popup.hide()
            return False
        else:
            return True

    def _on_owner_change(self,clip,event):
        text = self.primary.wait_for_text()
        if text != None:
            print text
        else:
            print("No text on the clipboard.")
            return False
        s,x,y,m=self.main_win.display.get_pointer()
        print "x= %f,y=%f" % (x,y)
        results=youdaoQuery.gettext(text)
        youdaoQuery.creat_file(text,results)
        self.popup.load_uri("file:///home/lcq/python/exercise/cache/"+text)
        self.popup.popup.move(x,y)
        self.popup.popup.show_all()
        center={'x':x,'y':y}
        Gdk.threads_add_timeout(GLib.PRIORITY_DEFAULT_IDLE,MOUSE_DETECT_INTERVAL,self._check_mouse,center)
        

def main():
    pop=Popup()
    win=MainWindow()
    clip=Clip(win,pop)
    Gtk.main()

if __name__ == "__main__":
    main()
