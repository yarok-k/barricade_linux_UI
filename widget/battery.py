import os
import psutil
class BatteryMonitor():
    def __init__(self):
        self.charge = 0
        self.status = False

    def update_scharging_status(self):
        plug_status = psutil.sensors_battery()
        if plug_status:
            self.status = True
            return True
        self.status =False
        return False

    def update_battery_charge(self):
        battery = psutil.sensors_battery()
        if battery is not None:
            percent = int(battery.percent)
            self.charge = percent
            print(percent)
            return percent
