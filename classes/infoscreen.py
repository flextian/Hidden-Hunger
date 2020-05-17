from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout


class InfoScreen(Screen):

    def on_enter(self, *args):
        self.ids.center_panel.ids.title_box.ids.title.text = "title changed"

    def go_back(self):
        self.manager.current = 'results_screen'