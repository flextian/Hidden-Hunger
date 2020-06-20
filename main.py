import os
import certifi
from kivy.base import EventLoop
from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, FadeTransition

Factory.register("MainScreen", module="classes.mainscreen")
Builder.load_file("kvs/mainscreen.kv")
Factory.register("ResultsScreen", module="classes.resultsscreen")
Builder.load_file("kvs/resultsscreen.kv")
Factory.register("InfoScreen", module="classes.infoscreen")
Builder.load_file("kvs/infoscreen.kv")

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["PGEOCODE_DATA_DIR"] = "pgeocode_data"


class UIManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition()


class HungerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.row = None
        self.manager = None
        EventLoop.window.bind(on_keyboard=self.back_button_handler)

    def back_button_handler(self, window, key, *args):
        if key == 27:
            if self.manager.current == 'info_screen':
                self.manager.get_screen("info_screen").go_back()
                return True
            elif self.manager.current == 'results_screen':
                self.manager.get_screen("results_screen").go_back()
                return True
            elif self.manager.current == 'main_screen':
                return False

    def build(self):
        self.title = "Caring Cranes"
        self.manager = UIManager()
        return self.manager


if __name__ == "__main__":
    HungerApp().run()
