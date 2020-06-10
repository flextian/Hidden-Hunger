import math
from os.path import join, dirname
import mysql.connector
import pgeocode
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapMarkerPopup
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from mysql.connector import errorcode
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
            opening_time=0,
            callback=self.set_item,
            position="auto",
        )
        self.ids.distance.set_item("15")

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
        icon_scroller = self.manager.get_screen("results_screen").ids.bank_icons

        # Get zip code data and check if valid
        zip_to_coords = pgeocode.Nominatim("us")
        zip_code_latitude = float(
            zip_to_coords.query_postal_code(self.zip_code).get("latitude")
        )
        # if the zip code doesnt have valid data / is invalid
        if math.isnan(zip_code_latitude):
            error_label = MDLabel(text="Invalid Zip Code!", halign="center")
            icon_scroller.add_widget(error_label)
            return
        zip_code_longitude = float(
            zip_to_coords.query_postal_code(self.zip_code).get("longitude")
        )
        self.zip_code_latitude = zip_code_latitude
        self.zip_code_longitude = zip_code_longitude

        # Connect to database
        try:
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
        except mysql.connector.Error as err:
            if err.errno == errorcode.CR_CONN_HOST_ERROR:
                connection_error_label = MDLabel(
                    text="No Internet Connection!", halign="center"
                )
                icon_scroller.add_widget(connection_error_label)
                return
            else:
                raise

        # Create and append cards
        for row in records:
            row = list(row)
            foodbank_distance = self.calculate_distance(
                row, zip_code_latitude, zip_code_longitude
            )
            # if the distance is greater than the threshold

            if foodbank_distance > float(self.distance_threshold):
                continue
            row.append(foodbank_distance)
            row.append(zip_code_latitude)
            row.append(zip_code_longitude)
            card = FoodbankIcon(row, self.manager)
            cards.append(card)
        cards = sorted(cards, key=lambda x: float(x.info[15]))
        for card in cards:
            icon_scroller.add_widget(card)

        if len(cards) == 0:
            no_results_label = MDLabel(text="No Results Found!", halign="center")
            icon_scroller.add_widget(no_results_label)

        self.create_zip_code_marker()

    def calculate_distance(self, row, latitude, longitude):
        distance = self.haversine(
            (latitude, longitude), (float(row[12]), float(row[13]))
        )
        return round((distance / 1000) * 0.621371, 2)

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
        map = self.manager.get_screen("info_screen").ids.map
        if self.zip_marker is not None:
            map.remove_widget(self.zip_marker)
        marker = MapMarkerPopup(
            lat=self.zip_code_latitude,
            lon=self.zip_code_longitude,
            source=join(dirname(__file__), "..", "sources", "person.png"),
        )
        map.add_widget(marker)
        self.zip_marker = marker
