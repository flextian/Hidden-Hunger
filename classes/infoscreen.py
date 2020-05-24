from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
import webbrowser
from kivy_garden.mapview import MapMarkerPopup


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

    def on_enter(self, *args):
        self.info = MDApp.get_running_app().row
        self.ids.center_panel.ids.title_box.ids.title.text = self.info[1]
        self.ids.center_panel.ids.list_box.ids.address.text = self.info[2]
        self.ids.center_panel.ids.information.text = self.info[14]
        self.ids.center_panel.ids.title_box.ids.distance.text = str(self.info[15]) + " Miles Away"

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
        print('calling')

    def go_back(self):
        self.map.remove_widget(self.marker)
        self.manager.current = 'results_screen'


class Marker(MapMarkerPopup):
    def __init__(self, lat, lon, map_widget, **kwargs):
        super().__init__(**kwargs)
        self.map = map_widget
        self.lat = lat
        self.lon = lon
        self.map.center_on(self.lat, self.lon)
        self.map.zoom = 17
        print('created')

    def on_release(self, *args):
        self.map.center_on(self.lat, self.lon)
        current_zoom = self.map.zoom
        print('pressed')
        # If the map is not zoomed in close enough, the map will zoom to the marker
        if current_zoom < 17:
            self.map.zoom = 17
