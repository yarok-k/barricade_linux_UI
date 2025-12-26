import os
import time
import subprocess
import re
import json
import yaml
import abstract.dropdown_menu
# Устанавливаем Wayland бэкенд ПЕРЕД импортом GTK
os.environ['GDK_BACKEND'] = 'wayland'
os.environ['XDG_SESSION_TYPE'] = 'wayland'
os.environ['WAYLAND_DISPLAY'] = 'wayland-1'

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, Gdk, GtkLayerShell, GLib
class Calendar(abstract.dropdown_menu.DropdownMenuComponent):
    def Draw(self):
        pass