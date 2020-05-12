from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown_menu = None
        Clock.schedule_once(lambda _: self.create_dropdown_menu())

    def create_dropdown_menu(self):
        menu_items = [{"text": "All"}, {"text": "50"}, {"text": "30"}, {"text": "15"}, {"text": "10"}, {"text": "5"}]
        self.dropdown_menu = MDDropdownMenu(
            caller=self.ids.distance, items=menu_items, width_mult=4, callback=self.set_item
        )
        print('dropdown created!')

    def set_item(self, instance):
        self.ids.distance.set_item(instance.text)
        Clock.schedule_once(lambda _: self.dropdown_menu.dismiss(), 0.3)

    def open_dropdown(self):
        print('pressed!')
        self.dropdown_menu.open()
