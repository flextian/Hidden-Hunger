from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
import mysql.connector
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
import pgeocode, math


class FoodbankIcon(MDCard):
    def __init__(self, info, manager, **kwargs):
        super().__init__(**kwargs)
        self.info = info
        self.manager = manager

        box_container = BoxLayout()
        title = MDLabel(text=info[1], font_style='H6', halign='center', font_size=10)
        distance = MDLabel(text=str(info[15]) + " Miles", font_style='H6', halign='center', font_size=10)
        box_container.add_widget(title)
        box_container.add_widget(distance)

        background_button = Button(background_color=[0, 0, 0, 0], on_release=self.enter_info_screen)

        anchor = AnchorLayout()
        anchor.add_widget(background_button)
        anchor.add_widget(box_container)

        self.add_widget(anchor)

    def enter_info_screen(self, _):
        MDApp.get_running_app().row = self.info
        self.manager.current = 'info_screen'


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zip_code = None

    def on_enter(self, *args):
        self.zip_code = self.manager.get_screen('main_screen').ids.zip_code.text
        print(self.zip_code)
        self.search()

    def search(self, *args):
        self.ids.bank_icons.clear_widgets()
        connection = mysql.connector.connect(
            host="foodbanks.cnwqm1nc27hx.us-east-2.rds.amazonaws.com",
            database='foodbanks',
            user="app_user",
            passwd="password"
        )
        query = "select * from foodbanks"
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            row = list(row)
            foodbank_distance = self.calculate_distance(row)
            row.append(foodbank_distance)
            card = FoodbankIcon(row, self.manager)
            self.ids.bank_icons.add_widget(card)

    def calculate_distance(self, row):
        zip_to_coords = pgeocode.Nominatim('us')
        latitude = float(zip_to_coords.query_postal_code(self.zip_code).get('latitude'))
        longitude = float(zip_to_coords.query_postal_code(self.zip_code).get('longitude'))
        distance = self.haversine((latitude, longitude), (float(row[12]), float(row[13])))
        return round((distance / 1000) * 0.621371, 2)

    def haversine(self, coord1, coord2):
        R = 6372800  # Earth radius in meters
        lat1, lon1 = coord1
        lat2, lon2 = coord2

        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = math.sin(dphi / 2) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def go_back(self):
        self.manager.current = 'main_screen'
