from zoneinfo import ZoneInfo
from datetime import datetime
import os
class clock:
    def __init__(self):
        if os.path.islink('/etc/localtime'):
            timezone_path = os.readlink('/etc/localtime')
            self.timezone = ZoneInfo(timezone_path.split('zoneinfo/')[-1])
        self.time_WOS = datetime.now(self.timezone).strftime("%H:%M")  
        self.time_WS = datetime.now(self.timezone).strftime("%H:%M:%S")
        self.time_WOS_12 = datetime.now(self.timezone).strftime("%-I:%M %p")
        self.time_WS_12 = datetime.now(self.timezone).strftime("%-I:%M:%S %p")
        
        
        days_dict = {
            0: {"ru": "пн", "en": "mon", "ru_full": "Понедельник", "en_full": "Monday"},
            1: {"ru": "вт", "en": "tue", "ru_full": "Вторник", "en_full": "Tuesday"},
            2: {"ru": "ср", "en": "wed", "ru_full": "Среда", "en_full": "Wednesday"},
            3: {"ru": "чт", "en": "thu", "ru_full": "Четверг", "en_full": "Thursday"},
            4: {"ru": "пт", "en": "fri", "ru_full": "Пятница", "en_full": "Friday"},
            5: {"ru": "сб", "en": "sat", "ru_full": "Суббота", "en_full": "Saturday"},
            6: {"ru": "вс", "en": "sun", "ru_full": "Воскресенье", "en_full": "Sunday"}
        }
        self.wd = days_dict[datetime.now(self.timezone).weekday()]
        self.date = datetime.now(self.timezone).strftime("%d %m %Y")
             




    def update_data(self):
        if os.path.islink('/etc/localtime'):
            timezone_path = os.readlink('/etc/localtime')
            self.timezone = ZoneInfo(timezone_path.split('zoneinfo/')[-1])
        self.time_WOS = datetime.now(self.timezone).strftime("%H:%M")  
        self.time_WS = datetime.now(self.timezone).strftime("%H:%M:%S")
        self.time_WOS_12 = datetime.now(self.timezone).strftime("%-I:%M %p")
        self.time_WS_12 = datetime.now(self.timezone).strftime("%-I:%M:%S %p")
        
        
        days_dict = {
            0: {"ru": "пн", "en": "mon", "ru_full": "Понедельник", "en_full": "Monday"},
            1: {"ru": "вт", "en": "tue", "ru_full": "Вторник", "en_full": "Tuesday"},
            2: {"ru": "ср", "en": "wed", "ru_full": "Среда", "en_full": "Wednesday"},
            3: {"ru": "чт", "en": "thu", "ru_full": "Четверг", "en_full": "Thursday"},
            4: {"ru": "пт", "en": "fri", "ru_full": "Пятница", "en_full": "Friday"},
            5: {"ru": "сб", "en": "sat", "ru_full": "Суббота", "en_full": "Saturday"},
            6: {"ru": "вс", "en": "sun", "ru_full": "Воскресенье", "en_full": "Sunday"}
        }
        self.wd = days_dict[datetime.now(self.timezone).weekday()]
        self.date = datetime.now(self.timezone).strftime("%d %m %Y")

        

clock()