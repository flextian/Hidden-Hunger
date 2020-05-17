from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
import mysql.connector
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class FoodbankIcon(MDCard):
    def __init__(self, info, **kwargs):
        super().__init__(**kwargs)

        title = MDLabel(text=info[1], font_style='H3', halign='center')
        background_button = Button(background_color=[0,0,0,0])

        anchor = AnchorLayout()
        anchor.add_widget(background_button)
        anchor.add_widget(title)

        self.add_widget(anchor)


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
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
            print(row)
            card = FoodbankIcon(row)
            self.ids.bank_icons.add_widget(card)

    def go_back(self):
        self.manager.current = 'main_screen'
