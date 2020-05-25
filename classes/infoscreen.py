from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
import webbrowser

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar

from classes.components.marker import Marker


# TODO: Fix the flickering in the map


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
        self.phone_number = None
        self.map = None
        self.marker = None

        self.phone_dialog = MDDialog(
            title="Phone Number",
            text="",
            buttons=[
                MDFlatButton(
                    text="Close",
                    text_color=MDApp.get_running_app().theme_cls.primary_color,
                    on_release=self.close_phone_number_dialog
                ),
                MDFlatButton(
                    text="Copy",
                    text_color=MDApp.get_running_app().theme_cls.primary_color,
                    on_release=self.copy_phone_number
                ),
            ],
        )

    def on_enter(self, *args):
        self.info = MDApp.get_running_app().row
        self.ids.center_panel.ids.title_box.ids.title.text = self.info[1]
        self.ids.center_panel.ids.list_box.ids.address.text = self.info[2]
        self.ids.center_panel.ids.information.text = self.info[14]
        self.ids.center_panel.ids.title_box.ids.distance.text = str(self.info[15]) + " Miles Away"

        self.phone_dialog.text = self.info[3]
        self.phone_dialog.size_hint_x = 0.8
        self.phone_dialog.size = 1, 200

        self.map = self.ids.map
        self.marker = Marker(float(self.info[12]), float(self.info[13]), self.map)
        self.map.add_widget(self.marker)

        # Disables the website button if there is no website
        self.url = self.info[4]
        if self.url is None:
            self.ids.center_panel.ids.buttons_box.ids.website_container.ids.website_button.disabled = True
            self.ids.center_panel.ids.buttons_box.ids.website_container.ids.website_button_text.text_color = \
                MDApp.get_running_app().theme_cls.disabled_hint_text_color
        else:
            self.ids.center_panel.ids.buttons_box.ids.website_container.ids.website_button.disabled = False
            self.ids.center_panel.ids.buttons_box.ids.website_container.ids.website_button_text.text_color = \
                MDApp.get_running_app().theme_cls.primary_color

        # Disables the call button if there is no phone number
        self.phone_number = self.info[3]
        if self.phone_number is None:
            self.ids.center_panel.ids.buttons_box.ids.call_container.ids.call_button.disabled = True
            self.ids.center_panel.ids.buttons_box.ids.call_container.ids.call_button_text.text_color = \
                MDApp.get_running_app().theme_cls.disabled_hint_text_color
        else:
            self.ids.center_panel.ids.buttons_box.ids.call_container.ids.call_button.disabled = False
            self.ids.center_panel.ids.buttons_box.ids.call_container.ids.call_button_text.text_color = \
                MDApp.get_running_app().theme_cls.primary_color

    def open_url(self):
        print('opened url')
        webbrowser.open(self.url)

    def call_number(self):
        self.phone_dialog.open()

    def copy_phone_number(self, _):
        Clipboard.copy(self.info[3])
        Snackbar(text="Copied to Clipboard!").show()

    def close_phone_number_dialog(self, _):
        self.phone_dialog.dismiss()

    def go_back(self):
        self.map.remove_widget(self.marker)
        self.manager.current = 'results_screen'
