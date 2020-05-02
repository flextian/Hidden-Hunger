from kivy.uix.screenmanager import Screen
import pgeocode

class MapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        self.map = self.manager.get_screen("map_screen").ids.map
        self.set_map_lat_lon()
        self.set_zoom()

    def get_zipcode(self):
        return self.manager.get_screen("main_screen").ids.zip_code.text

    def get_zoom(self):
        return self.manager.get_screen("main_screen").ids.distance.text

    def set_map_lat_lon(self):
        zip = self.get_zipcode()
        zip_to_coords = pgeocode.Nominatim('us')
        latitude = float(zip_to_coords.query_postal_code(zip).get('latitude'))
        longitude = float(zip_to_coords.query_postal_code(zip).get('longitude'))

        # Setting the latitude and longitude on the map
        self.map.center_on(latitude, longitude)

    def set_zoom(self):
        miles_away = self.get_zoom()
        if miles_away == 'All':
            self.map.zoom = 6
        else:
            if int(miles_away) == 5:
                self.map.zoom = 12
            elif int(miles_away) == 15:
                self.map.zoom = 10
            elif int(miles_away) == 30:
                self.map.zoom = 9
            else:
                self.map.zoom = 8