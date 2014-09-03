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

        item = Gtk.CheckMenuItem.new_with_label("网络释义")
        item.set_active(self.clip.isNet)
        item.connect("toggled",self.cb_isNet)
        self.menu.append(item)
        self.use_web_item = item

        item = Gtk.MenuItem()
        item.set_label("退出")
        item.connect("activate",self.cb_quit)
        self.menu.append(item)

        self.menu.show_all()
        self.ind.set_menu(self.menu)

    def toggled(self,item,isNet=None):
        if isNet is None:
            return
        item.set_active(isNet)  #as same as emit a "toggled"

    def cb_isNet(self,widget):
        self.clip.change_net_state(widget.get_active())

    def cb_quit(self,widget):
        self.main_win._on_delete_event()


                
