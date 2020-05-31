from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class FoodbankIcon(MDCard):
    def __init__(self, info, manager, **kwargs):
        super().__init__(**kwargs)
        self.info = info
        self.manager = manager

        box_container = BoxLayout()
        title = MDLabel(text=info[1], font_style="H6", halign="center", font_size=10)
        distance = MDLabel(
            text=str(info[15]) + " Miles",
            font_style="H6",
            halign="center",
            font_size=10,
        )
        box_container.add_widget(title)
        box_container.add_widget(distance)

        background_button = Button(
            background_color=[0, 0, 0, 0], on_release=self.enter_info_screen
        )

        anchor = AnchorLayout()
        anchor.add_widget(background_button)
        anchor.add_widget(box_container)

        self.add_widget(anchor)

    def enter_info_screen(self, _):
        MDApp.get_running_app().row = self.info
        self.manager.current = "info_screen"
