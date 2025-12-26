import subprocess
import json

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk

class opened_apps:
    def __init__(self, container=None):
        self.apps = []
        self.container = container  # храним ссылку на контейнер
        self.windows_data = {}  # Словарь для хранения данных о окнах
        
        result = subprocess.run(
            ['hyprctl', 'clients', '-j'],
            capture_output=True,
            text=True,
            timeout=1
        )  
        if result.returncode == 0:
            clients = json.loads(result.stdout)
            for client in clients:
                app = self.create_app_button(client)
                self.apps.append(app)
                # Если контейнер передан, сразу добавляем кнопку
                if self.container:
                    self.container.pack_start(app, False, False, 0)

    def create_app_button(self, client):
        """Создает кнопку для приложения с обработчиком клика"""
        app = Gtk.Button(label=f"{client['class']}")
        app.set_valign(Gtk.Align.CENTER) 
        app.set_margin_start(10)
        app.set_margin_end(10)
        
        # Сохраняем данные окна в атрибуты кнопки
        app.address = client.get('address', '')  # Адрес окна в Hyprland
        app.class_name = client.get('class', '')
        app.title = client.get('title', '')
        
        # Добавляем обработчик клика
        app.connect("clicked", self.on_app_clicked)
        
        # Сохраняем данные окна для быстрого доступа
        self.windows_data[client['address']] = {
            'class': client['class'],
            'title': client.get('title', ''),
            'address': client['address']
        }
        
        return app
    
    def on_app_clicked(self, button):
        """Обработчик клика по кнопке приложения"""
        if hasattr(button, 'address') and button.address:
            # Используем адрес окна для фокусировки
            subprocess.run(['hyprctl', 'dispatch', 'focuswindow', f'address:{button.address}'])

    def update(self, container):
        self.container = container
        # Добавляем все существующие кнопки в новый контейнер
        for app in self.apps:
            self.container.pack_start(app, False, False, 0)

        if not self.container:
            return False
            
        result = subprocess.run(
            ['hyprctl', 'clients', '-j'],
            capture_output=True,
            text=True,
            timeout=1
        )  
        if result.returncode == 0:
            clients = json.loads(result.stdout)
            
            # Получаем текущие адреса окон из hyprctl
            current_addresses = [client["address"] for client in clients]
            
            # Получаем текущие адреса из self.apps
            current_button_addresses = []
            for button in self.apps:
                if hasattr(button, 'address'):
                    current_button_addresses.append(button.address)
            
            # Получаем текущие кнопки из контейнера для проверки
            container_buttons = self.container.get_children()
            
            # Удаляем кнопки для закрытых приложений
            apps_to_remove = []
            for i, button in enumerate(self.apps):
                if hasattr(button, 'address') and button.address not in current_addresses:
                    apps_to_remove.append(i)
            
            # Удаляем в обратном порядке, чтобы индексы не сдвигались
            for i in reversed(apps_to_remove):
                # Удаляем кнопку из контейнера и уничтожаем ее
                if self.apps[i] in container_buttons:
                    self.container.remove(self.apps[i])
                # Удаляем данные окна
                if hasattr(self.apps[i], 'address') and self.apps[i].address in self.windows_data:
                    del self.windows_data[self.apps[i].address]
                self.apps[i].destroy()
                del self.apps[i]
            
            # Добавляем кнопки для новых приложений
            for client in clients:
                client_address = client["address"]
                if client_address not in current_button_addresses:
                    app = self.create_app_button(client)
                    self.apps.append(app)
                    self.container.pack_end(app, False, False, 0)
            
            # Обновляем данные для существующих окон (на случай изменения заголовка и т.д.)
            for client in clients:
                if client['address'] in self.windows_data:
                    self.windows_data[client['address']].update({
                        'title': client.get('title', ''),
                        'class': client['class']
                    })
            
            # Обновляем отображение контейнера
            self.container.show_all()