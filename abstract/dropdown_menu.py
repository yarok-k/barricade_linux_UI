import os
import time
import subprocess
import re
import json
import yaml
import abstract.basic_methods
# Устанавливаем Wayland бэкенд ПЕРЕД импортом GTK
os.environ['GDK_BACKEND'] = 'wayland'
os.environ['XDG_SESSION_TYPE'] = 'wayland'
os.environ['WAYLAND_DISPLAY'] = 'wayland-1'

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, GtkLayerShell
class DropdownMenuComponent(Gtk.Window,abstract.basic_methods.BaseComponent):
    def __init__(self, parent_bar, size:tuple, space:int,pos:int):
        self.toggle_position = False
        Gtk.Window.__init__(self, title="")
        self.parent_bar = parent_bar
        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.OVERLAY)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
        match pos:
            case 1:
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
            case 2:
                pass
            case 3:
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)
        panel_height = parent_bar.get_allocated_height()
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, panel_height)
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.RIGHT, parent_bar.height+space)
        self.set_default_size(size[0],size[1])
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_name("dropdown_menu")
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.main_box.set_margin_top(10)
        self.main_box.set_margin_bottom(10)
        self.main_box.set_margin_start(10)
        self.main_box.set_margin_end(10)
        self.Draw()
        self.add(self.main_box)
        self.LoadStyle("/home/yarok/.config/yarok_bar_dock/style.css")

    
