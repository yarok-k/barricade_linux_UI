
import yaml
import re
import subprocess
class network():
    def __init__(self):
        self.status = 0
    
    def update_network_status(self):
        result = subprocess.run(
            ['nmcli', '-t', '-f', 'DEVICE,TYPE,STATE,CONNECTION', 'device', 'status'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode==0:
            with open('/home/yarok/.config/yarok_bar_dock/config.yaml', 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            lines = []
            for line in result.stdout.strip().split('\n'):
                lines.append(line.lower())
            
            if any(":connected:" in line for line in lines) and any(":wired" in line for line in lines):
                self.network_display.set_label("L")
                return True
            elif any(":connected:" in line for line in lines) and any(":wired" not in line for line in lines):
                for line in [line for line in lines if ":connected:" in line and ":wired" not in line]:
                    if data.get("WI-FI"):
                        interface = line[:line.index(":")]
                        result = subprocess.run(
                            ['iw', 'dev', interface, 'link'],
                            capture_output=True,
                            text=True,
                            timeout=1
                        )
                        if result.returncode == 0:
                            for line in result.stdout.split('\n'):
                                if "signal:" in line.lower():
                                    match = re.search(r'[-]?\d+', line)
                                    if match:
                                        dbm = int(match.group())
                                        if dbm >= -50:
                                            self.status = "5"
                                        elif dbm >= -60:
                                            self.status = "4"
                                        elif dbm >= -70:
                                            self.status = "3"
                                        elif dbm >= -80:
                                            self.status = "2"
                                        else:
                                            self.status = "1"
                                        return True
                        return True
                    return True
                else:
                    self.status = " "         
                    return True
        return True