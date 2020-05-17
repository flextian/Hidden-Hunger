from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import mysql.connector
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu


class FoodbankIcon(MDCard):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        title = MDLabel(text=name)
        self.add_widget(title)




class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        self.search()

    def search(self, *args):
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
            print(row)
            card = FoodbankIcon(row[1])
            self.ids.bank_icons.add_widget(card)

    def go_back(self):
        self.manager.current = 'main_screen'
