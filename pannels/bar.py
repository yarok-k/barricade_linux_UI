import os
import time
import subprocess
import re
import json
import yaml
import dropdown_menues.quick_settings as qs 
import dropdown_menues.calendar as cal
import abstract.pannel_menu
import widget.keyboard as keyboard
import widget.network as net
import widget.clock as clock
import widget.battery as batt
# Устанавливаем Wayland бэкенд ПЕРЕД импортом GTK
os.environ['GDK_BACKEND'] = 'wayland'
os.environ['XDG_SESSION_TYPE'] = 'wayland'
os.environ['WAYLAND_DISPLAY'] = 'wayland-1'

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, GLib
class Bar(abstract.pannel_menu.PannelComponent):
    def Draw(self):
        self.calendar = cal.Calendar(self,(200,200),10,2)
        self.quick_settings = qs.quicksettings_menu(self,(200,200),10,3)
        # блок с иконками располагающимися слева
        self.left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.left_box.set_valign(Gtk.Align.CENTER)
        self.left_box.set_halign(Gtk.Align.CENTER)
        self.left_box.set_name("bar_left_section")
        
        # блок с иконками располагающимися по центру
        self.center_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.center_box.set_valign(Gtk.Align.CENTER)
        self.center_box.set_halign(Gtk.Align.CENTER)
        self.center_box.set_name("bar_center_section")
        self.main_box.set_center_widget(self.center_box)
        # блок с иконками располагающимися справа
        self.right_box_event = Gtk.Button()
        self.right_box_event.set_valign(Gtk.Align.CENTER)
        self.right_box_event.set_halign(Gtk.Align.CENTER)
        self.right_box_event.set_margin_start(10)
        self.right_box_event.set_name("bar_right_section")
        self.right_box_event.connect("clicked", lambda qq: self.quick_settings.Toggle())

        self.right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.right_box.set_valign(Gtk.Align.CENTER)
        self.right_box.set_halign(Gtk.Align.CENTER)
        self.right_box.set_margin_start(10)
        self.right_box_event.add(self.right_box)


        self.keyboard = keyboard.keyboard()
        self.net = net.network()
        self.clock = clock.clock()
        self.battety = batt.BatteryMonitor()
    #<<==<<виджеты левого контейнера>>==>>
        # кнопка старт справа панели
        self.StartButton = Gtk.Button(label="start")
        self.StartButton.set_valign(Gtk.Align.CENTER)
        self.StartButton.set_margin_start(10)
        self.StartButton.set_margin_end(10)
        self.StartButton.connect("clicked", lambda mm: subprocess.run("nwg-drawer"))
        self.StartButton.set_name("start")
    #<<==<<виджеты центрального контейнера>>==>>
        # часы по центру панели
        self.DateTime = Gtk.Button()
        self.DateTime.set_valign(Gtk.Align.CENTER)
        self.DateTime.set_margin_start(10)
        self.DateTime.set_margin_end(10)
        self.DateTime.set_name("clock")
        self.DateTime.connect("clicked", lambda sc: self.calendar.Toggle())
    #<<==<<виджеты правого контейнера>>==>>
        # показывает текущую раскладку
        self.keyboard_layout_display = Gtk.Label()
        self.keyboard_layout_display.set_valign(Gtk.Align.CENTER)
        self.keyboard_layout_display.set_margin_start(10)
        self.keyboard_layout_display.set_margin_end(10)
        # показывает тсостояние caps и num lock
        self.keyboard_caps_display = Gtk.Label(label="   ")
        self.keyboard_caps_display.set_valign(Gtk.Align.CENTER)
        self.keyboard_caps_display.set_margin_start(10)
        self.keyboard_caps_display.set_margin_end(10)
        # показывает стватус сети (wifi+ур сигнала или проводная сеть)
        self.network_display = Gtk.Label()
        self.network_display.set_valign(Gtk.Align.CENTER)
        self.network_display.set_margin_start(10)
        self.network_display.set_margin_end(10)
        # показывает текущий заряд батареи
        self.battery_display = Gtk.Label()
        self.battery_display.set_valign(Gtk.Align.CENTER)
        self.battery_display.set_margin_start(10)
        self.battery_display.set_margin_end(10)



        #наполнение левого контейнера
        self.left_box.pack_start(self.StartButton,False,False,0)
        #наполнение сентрального контейнера
        self.center_box.pack_start(self.DateTime,False,False,0)
        #наполнение правого контейнера
        self.right_box.pack_start(self.keyboard_layout_display,False,False,0)
        self.right_box.pack_start(self.keyboard_caps_display,False,False,0)
        self.right_box.pack_start(self.network_display,False,False,0)
        self.right_box.pack_start(self.battery_display,False,False,0)
        


        
        #обработка тиковых событий
        GLib.timeout_add(800,self.update_clock)
        GLib.timeout_add(100,self.update_keyboard_layout)
        GLib.timeout_add(800,self.update_network_status)
        GLib.timeout_add(800,self.update_battery_status)
    
        self.main_box.pack_start(self.left_box,False,False,0)
        #self.main_box.pack_start(SpacerL,False,False,0)
        self.main_box.pack_start(self.center_box,False,False,0)
        #self.main_box.pack_start(SpacerR,False,False,0)
        self.main_box.pack_end(self.right_box_event,False,False,0)
        self.add(self.main_box)

    def update_clock(self):
        self.clock.update_data()
        self.DateTime.set_label(f"{self.clock.date} | {self.clock.time_WS_12}")
        return True

    def update_keyboard_layout(self):
        self.keyboard.update_data()
        self.keyboard.update_layout()
        self.keyboard.update_caps_status()
        self.keyboard.update_num_status()
        self.keyboard_layout_display.set_label(self.keyboard.get_layout())
        if self.keyboard.get_caps_lock()==True and self.keyboard.get_num_lock()==True:
            self.keyboard_caps_display.set_label("C N")
        elif self.keyboard.get_caps_lock()==True and self.keyboard.get_num_lock()==False:
            self.keyboard_caps_display.set_label("C  ")
        elif self.keyboard.get_caps_lock()==False and self.keyboard.get_num_lock()==True:
            self.keyboard_caps_display.set_label("  N")
        else:
            self.keyboard_caps_display.set_label("   ")
        return True

    def update_network_status(self):
        self.net.update_network_status()
        self.network_display.set_label(self.net.status)

    def update_battery_status(self):
        self.battety.update_battery_charge()
        self.battety.update_scharging_status()
        if not self.battety.status:
            self.battery_display.set_label("P")
        else:
            self.battery_display.set_label(f"{self.battety.charge}")

        
        