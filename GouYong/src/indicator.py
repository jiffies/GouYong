#!-*- coding:utf-8 -*-
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
import os.path
import dict_manager
INDICATOR_NAME = "GouYong"
class DictIndicator(object):
    def __init__(self,main_win,clip,dm):
        self.name=INDICATOR_NAME
        self.main_win= main_win
        self.clip = clip
        self.dm = dm
        self.ind = appindicator.Indicator.new_with_path(
                    self.name,
                    "icon",
                    appindicator.IndicatorCategory.APPLICATION_STATUS,
                    os.path.join(os.path.dirname(__file__),'..'))
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.menu = Gtk.Menu()

        item = Gtk.CheckMenuItem.new_with_label("网络释义")
        item.set_active(self.clip.isNet)
        item.connect("toggled",self.cb_isNet)
        self.menu.append(item)
        self.use_web_item = item

        self.init_submenu()

        item = Gtk.MenuItem()
        item.set_label("退出")
        item.connect("activate",self.cb_quit)
        self.menu.append(item)

        self.menu.show_all()
        self.ind.set_menu(self.menu)


    def init_submenu(self):
        dict_select = Gtk.Menu()
        item = Gtk.MenuItem()
        item.set_label("选择词典")
        item.set_submenu(dict_select)
        self.menu.append(item)

        self.dict_select_group = Gtk.RadioMenuItem().get_group()
        for dict in self.dm.dicts:
            item = Gtk.RadioMenuItem.new_with_label(self.dict_select_group,dict)
            if dict == dict_manager.DEFAULT:
                item.set_active(True)
            self.dict_select_group = item.get_group()
            #item.set_label(dict)
            item.connect("toggled",self.cb_dict_select)
            dict_select.append(item)

    def cb_dict_select(self,widget):
        if not widget.get_active():
            print "%s not selected" % widget.get_label()
            return
        self.dm.change_dict(widget.get_label())
        

    def toggled(self,item,isNet=None):
        if isNet is None:
            return
        item.set_active(isNet)  #as same as emit a "toggled"

    def cb_isNet(self,widget):
        self.clip.change_net_state(widget.get_active())

    def cb_quit(self,widget):
        self.main_win._on_delete_event()


                
