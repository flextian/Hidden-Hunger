import os
import certifi
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

os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ["PGEOCODE_DATA_DIR"] = 'pgeocode_data'

class UIManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition()


class HungerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.row = None

    def build(self):
        self.title = "Caring Cranes"
        return UIManager()


if __name__ == "__main__":
    HungerApp().run()
