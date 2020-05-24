from kivy_garden.mapview import MapMarkerPopup


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