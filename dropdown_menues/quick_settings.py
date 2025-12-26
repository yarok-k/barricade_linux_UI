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
class quicksettings_menu(abstract.dropdown_menu.DropdownMenuComponent):
    def Draw(self):
        self.wifi = Gtk.ComboBoxText()
        self.get_wifi_networks()
        self.main_box.add(self.wifi)

    def get_wifi_networks(self):
        """
        Сканирует доступные Wi‑Fi сети с помощью системных команд через subprocess.
        Результаты добавляются в self.wifi (предполагается, что это виджет с методом append_text).
        """
        result = subprocess.run(
            ['nmcli', '-f', 'SSID', 'dev', 'wifi', 'list'],
            capture_output=True, text=True, check=True
        )
        output = result.stdout
        print(output)
        # Извлекаем SSID (учитываем возможные пробелы в названии сети)
        for line in output.strip().split('\n')[1:]:  # пропускаем заголовок
            if line.strip():
                # SSID — всё, что не является пробелами в начале строки до следующих пробелов/табов
                ssid = re.match(r'^\s*(\S.*?)\s*$', line)
                if ssid and ssid.group(1)!="--":
                    self.wifi.append_text(ssid.group(1))
        return True