from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
import webbrowser


class InfoScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.info = None
        '''
        0 = id
        1 = name
        2 = address
        3 = phone number
        4 = website
        5 to 11 = Monday - Friday
        12 = latitude
        13 = longitude
        14 = information
        15 = distance in miles
        '''
        self.url = None


    def on_enter(self, *args):
        self.info = MDApp.get_running_app().row
        self.ids.center_panel.ids.title_box.ids.title.text = self.info[1]
        self.ids.center_panel.ids.list_box.ids.address.text = self.info[2]
        self.ids.center_panel.ids.information.text = self.info[14]
        self.ids.center_panel.ids.title_box.ids.distance.text = str(self.info[15]) + " Miles Away"

        self.url = self.info[4]

    def open_url(self):
        print('opened url')

    def go_back(self):
        self.manager.current = 'results_screen'
