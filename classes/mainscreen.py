import math
from os.path import join, dirname

import mysql.connector
import pgeocode
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapMarkerPopup
from kivymd.uix.menu import MDDropdownMenu

from classes.components.foodbankicon import FoodbankIcon


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown_menu = None
        self.zip_code = None
        self.zip_code_latitude = None
        self.zip_code_longitude = None
        self.distance_threshold = None
        self.zip_marker = None
        Clock.schedule_once(lambda _: self.create_dropdown_menu())

    def create_dropdown_menu(self):
        menu_items = [
            {"text": "All"},
            {"text": "50"},
            {"text": "30"},
            {"text": "15"},
            {"text": "10"},
            {"text": "5"},
        ]
        self.dropdown_menu = MDDropdownMenu(
            caller=self.ids.distance,
            items=menu_items,
            width_mult=4,
            callback=self.set_item,
            position="auto",
        )
        self.ids.distance.set_item("All")

    # TODO: Fix the fact that if you spam the button you crash the program.
    def set_item(self, instance):
        self.ids.distance.set_item(instance.text)
        Clock.schedule_once(lambda _: self.dropdown_menu.dismiss(), 0.3)

    def open_dropdown(self):
        self.dropdown_menu.open()

    # All methods below are ran when the submit button is clicked <---------------------------------------------------->
    def get_results(self):
        self.manager.current = "results_screen"
        self.zip_code = self.ids.zip_code.text
        self.distance_threshold = self.ids.distance.current_item
        Clock.schedule_once(lambda _: self.search())

    def search(self, *args):
        cards = []

        self.manager.get_screen("results_screen").ids.bank_icons.clear_widgets()
        connection = mysql.connector.connect(
            host="foodbanks.cnwqm1nc27hx.us-east-2.rds.amazonaws.com",
            database="foodbanks",
            user="app_user",
            passwd="password",
        )

        query = "select * from foodbanks"
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            row = list(row)
            foodbank_distance, zip_code_latitude, zip_code_longitude = self.calculate_distance(row)

            # if the distance is greater than the threshold
            if self.distance_threshold is not "All":
                if foodbank_distance > float(self.distance_threshold):
                    continue

            row.append(foodbank_distance)
            self.zip_code_latitude = zip_code_latitude
            self.zip_code_longitude = zip_code_longitude
            row.append(zip_code_latitude)
            row.append(zip_code_longitude)
            card = FoodbankIcon(row, self.manager)
            cards.append(card)

        cards = sorted(cards, key=lambda x: float(x.info[15]))

        for card in cards:
            self.manager.get_screen("results_screen").ids.bank_icons.add_widget(card)

        self.create_zip_code_marker()

    def calculate_distance(self, row):
        zip_to_coords = pgeocode.Nominatim("us")
        latitude = float(zip_to_coords.query_postal_code(self.zip_code).get("latitude"))
        longitude = float(
            zip_to_coords.query_postal_code(self.zip_code).get("longitude")
        )
        distance = self.haversine(
            (latitude, longitude), (float(row[12]), float(row[13]))
        )
        return round((distance / 1000) * 0.621371, 2), latitude, longitude

    def haversine(self, coord1, coord2):
        R = 6372800  # Earth radius in meters
        lat1, lon1 = coord1
        lat2, lon2 = coord2

        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = (
                math.sin(dphi / 2) ** 2
                + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        )

        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def create_zip_code_marker(self):
        map = self.manager.get_screen('info_screen').ids.map
        if self.zip_marker is not None:
            map.remove_widget(self.zip_marker)
        marker = MapMarkerPopup(lat=self.zip_code_latitude, lon=self.zip_code_longitude, source=join(dirname(__file__), "..", "sources", "person.png"))
        map.add_widget(marker)
        self.zip_marker = marker
