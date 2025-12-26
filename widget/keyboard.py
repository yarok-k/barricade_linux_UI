import subprocess
import json
class keyboard:
    def __init__(self):
        self.layout = "en"
        self.caps = False
        self.num = False
        self.result =  subprocess.run(
            ['hyprctl', 'devices', '-j'],
            capture_output=True,
            text=True,
            timeout=1
        )

    def update_layout(self):
        if self.result.returncode == 0:
            data = json.loads(self.result.stdout)
            for device in data.get('keyboards', []):
                if device["main"]:
                    match (str(device["active_keymap"])):
                        case "English (US)":
                            self.layout = "en"
                        case "Russian":
                            self.layout = "ru"
        else:
            self.layout = "??"
            return True
        
    def update_caps_status(self):
        if self.result.returncode == 0:
            data = json.loads(self.result.stdout)
            for device in data.get('keyboards', []):
                if device["main"]:
                    if (device["capsLock"]==True):
                        self.caps = True
                    else:
                        self.caps = False
                    return True
        else:
            return True
    
    def update_num_status(self):
        if self.result.returncode == 0:
            data = json.loads(self.result.stdout)
            for device in data.get('keyboards', []):
                if device["main"]:
                    if (device["numLock"]==True):
                        self.num = True
                    else:
                        self.num = False
                    return True
        else:
            return True
        
    def update_data(self):
        self.result =  subprocess.run(
            ['hyprctl', 'devices', '-j'],
            capture_output=True,
            text=True,
            timeout=1
        )
    
    def get_layout(self):
        return self.layout

    def get_caps_lock(self):
        return self.caps
    
    def get_num_lock(self):
        return self.num