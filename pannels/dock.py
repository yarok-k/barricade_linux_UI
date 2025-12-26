import os
import subprocess
import json
import abstract.pannel_menu
import widget.opened_apps as opened
# Устанавливаем Wayland бэкенд ПЕРЕД импортом GTK
os.environ['GDK_BACKEND'] = 'wayland'
os.environ['XDG_SESSION_TYPE'] = 'wayland'
os.environ['WAYLAND_DISPLAY'] = 'wayland-1'

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, GLib

class Dock(abstract.pannel_menu.PannelComponent):
    def Draw(self):
        self.opened = opened.opened_apps()
        

        self.process_list = []
        self.apps_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.start_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.StartButton = Gtk.Button(label="start")
        self.StartButton.set_valign(Gtk.Align.CENTER) 
        self.StartButton.set_margin_start(10)
        self.StartButton.set_margin_end(10)
        self.StartButton.connect("clicked", lambda mm: subprocess.run("nwg-drawer"))
        self.StartButton.set_name("start_button_dock")

        GLib.timeout_add(500,self.update_processes_butts)
        
        self.start_button_box.pack_start(self.StartButton,False,False,0)

        self.main_box.pack_start(self.apps_box,False,False,0)
        self.main_box.pack_start(self.start_button_box,False,False,0)
        self.add(self.main_box)
    
    def update_processes_butts(self):
        self.opened.update(self.apps_box)
        return True