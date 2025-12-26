import os

os.environ['GDK_BACKEND'] = 'wayland'
os.environ['XDG_SESSION_TYPE'] = 'wayland'
os.environ['WAYLAND_DISPLAY'] = 'wayland-1'

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk
import pannels.dock as dock
import pannels.bar as bar
if __name__ == "__main__":    
    dock_pannel = dock.Dock(80,False,"dock")
    top_bar = bar.Bar(30,True,"bar")
    dock_pannel.connect("destroy", Gtk.main_quit)
    top_bar.connect("destroy", Gtk.main_quit)
    dock_pannel.show_all()
    top_bar.show_all()
    Gtk.main()