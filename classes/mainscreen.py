import math

import mysql.connector
import pgeocode
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu


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


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown_menu = None
        self.zip_code = None
        Clock.schedule_once(lambda _: self.create_dropdown_menu())

    def create_dropdown_menu(self):
        menu_items = [{"text": "All"}, {"text": "50"}, {"text": "30"}, {"text": "15"}, {"text": "10"}, {"text": "5"}]
        self.dropdown_menu = MDDropdownMenu(
            caller=self.ids.distance, items=menu_items, width_mult=4, callback=self.set_item, position='auto'
        )
        print('dropdown created!')

    # TODO: Fix the fact that if you spam the button you crash the program.
    def set_item(self, instance):
        self.ids.distance.set_item(instance.text)
        Clock.schedule_once(lambda _: self.dropdown_menu.dismiss(), 0.3)

    def open_dropdown(self):
        print('pressed!')
        self.dropdown_menu.open()

    # All methods below are ran when the submit button is clicked
    def get_results(self):
        self.manager.current = 'results_screen'
        self.zip_code = self.ids.zip_code.text
        print(self.zip_code)
        # TODO: Make the search process asynchronous (enter the results screen first, then load)
        self.search()

    def search(self, *args):
        cards = []

        self.manager.get_screen('results_screen').ids.bank_icons.clear_widgets()
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
            cards.append(card)

        cards = sorted(cards, key=lambda x: float(x.info[15]))

        for card in cards:
            self.manager.get_screen('results_screen').ids.bank_icons.add_widget(card)

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