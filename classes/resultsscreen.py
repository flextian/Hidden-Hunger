from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go_back(self):
        self.manager.current = 'main_screen'