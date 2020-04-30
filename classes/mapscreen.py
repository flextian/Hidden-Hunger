from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapView
import pgeocode


class MapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        self.set_map_lat_lon()

    def get_zipcode(self):
        return self.manager.get_screen("main_screen").ids.zip_code.text

    def set_map_lat_lon(self):
        zip = self.get_zipcode()
        zip_to_coords = pgeocode.Nominatim('us')
        latitude = float(zip_to_coords.query_postal_code(zip).get('latitude'))
        longitude = float(zip_to_coords.query_postal_code(zip).get('longitude'))

        # Setting the latitude and longitude on the map
        self.manager.get_screen("map_screen").ids.map.center_on(latitude, longitude)
