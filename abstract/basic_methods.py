import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')

#импорт gtk
from gi.repository import Gtk, Gdk, GtkLayerShell, GLib
class BaseComponent:
    def Draw(self):
        """
        !!! МЕТОД ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ !!!
        Здесь мы прописываем вёрстку интерфейса
        """
        pass


    def LoadStyle(self,stylesheet_file:str):
        """
        :param stylesheet_file: Путь до css файла со стилями доя меню
        :type stylesheet_file: str
        обязательные поля:
        dropdown_menu: стиль самого меню
        """
        provider = Gtk.CssProvider()
        provider.load_from_path(stylesheet_file)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    def Toggle(self):
        print(self.toggle_position)
        if not(self.toggle_position):
            self.set_sensitive(True)
            self.show_all()
            self.toggle_position = not(self.toggle_position)
        else:
            self.hide()
            self.set_sensitive(False)
            self.toggle_position = not(self.toggle_position)