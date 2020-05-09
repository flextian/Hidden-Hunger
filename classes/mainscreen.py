from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # TODO: Make it so that a new dropdown is not made everytime it is pressed! Its slow!
    def open_dropdown(self):
        print(self.ids.distance)
        menu_items = [{"icon": "git", "text": f"Item {i}"} for i in range(5)]
        self.dropdown = MDDropdownMenu(
            caller=self.ids.distance, items=menu_items, width_mult=4
        )
        self.dropdown.open()
