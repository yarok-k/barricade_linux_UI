import os
import abstract.basic_methods
# wayland как бекенд
os.environ['GDK_BACKEND'] = 'wayland'
os.environ['XDG_SESSION_TYPE'] = 'wayland'
os.environ['WAYLAND_DISPLAY'] = 'wayland-1'

#активация gtk
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')

#импорт gtk
from gi.repository import Gtk, GtkLayerShell

class PannelComponent(Gtk.Window,abstract.basic_methods.BaseComponent):
    def __init__(self,height:int,pos:bool,name:str):
        self.toggle_position = False
        Gtk.Window.__init__(self, title="")
        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.TOP)
        if pos:
            GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
            GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
            GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)
        else:
            GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, True)
        GtkLayerShell.set_exclusive_zone(self, height)
        self.height = height
        self.set_default_size(-1, height)
        self.set_resizable(False)
        self.set_decorated(False)
        self.set_app_paintable(True)
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_box.set_size_request(-1, height)
        self.main_box.set_name(name)
        self.Draw()
        self.set_size_request(-1, height)
        self.LoadStyle("/home/yarok/.config/yarok_bar_dock/style.css")
