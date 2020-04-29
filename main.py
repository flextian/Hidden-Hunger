from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import FadeTransition, ScreenManager
from kivy.config import Config
from kivy.core.window import Window

Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '568')
Config.write()

Factory.register("MainScreen", module="classes.mainscreen")
Builder.load_file("kvs/mainscreen.kv")


class UIManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition()


class HungerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = "Hungry Hippos"
        return UIManager()


if __name__ == "__main__":
    HungerApp().run()
