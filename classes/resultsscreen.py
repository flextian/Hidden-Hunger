from kivy.uix.screenmanager import Screen
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zip_code = None

    def go_back(self):
        self.ids.bank_icons.clear_widgets()
        self.manager.current = "main_screen"


class CustomToolbar(
    ThemableBehavior, RectangularElevationBehavior, MDBoxLayout,
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = self.theme_cls.primary_color
