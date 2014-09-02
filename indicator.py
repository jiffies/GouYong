#!-*- coding:utf-8 -*-
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
import os.path
INDICATOR_NAME = "GouYong"
class DictIndicator(object):
    def __init__(self,main_win,clip):
        self.name=INDICATOR_NAME
        self.main_win= main_win
        self.clip = clip
        self.ind = appindicator.Indicator.new_with_path(
                    self.name,
                    "icon",
                    appindicator.IndicatorCategory.APPLICATION_STATUS,
                    os.path.dirname(os.path.realpath(__file__)))
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.menu = Gtk.Menu()

        item = Gtk.MenuItem()
        item.set_label("网络释义")
        item.connect("activate",self.cb_isNet)
        self.menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("退出")
        item.connect("activate",self.cb_quit)
        self.menu.append(item)

        self.menu.show_all()
        self.ind.set_menu(self.menu)

    def cb_isNet(self,*args):
        self.clip.isNet ^= True

    def cb_quit(self,*args):
        self.main_win._on_delete_event()

                
