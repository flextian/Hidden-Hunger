from os.path import dirname, join

from kivy_garden.mapview import MapMarkerPopup


class Marker(MapMarkerPopup):
    def __init__(self, lat, lon, map_widget, ideal_zoom, **kwargs):
        super().__init__(**kwargs)
        self.map = map_widget
        self.lat = lat
        self.lon = lon
        self.ideal_zoom = ideal_zoom
        self.source = join(dirname(__file__), "..", "..", "sources", "location.png")

    def on_release(self, *args):
        self.map.center_on(self.lat, self.lon)
        self.map.zoom = self.ideal_zoom + 2
