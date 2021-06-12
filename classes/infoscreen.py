import datetime
import math
import webbrowser

try:
    from jnius import autoclass
    from jnius.jnius import cast
except Exception as e:
    print('on pc')

from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.utils import get_hex_from_color
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar

from classes.components.marker import Marker


class InfoScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.info = None
        """
        0 = id
        1 = name
        2 = address
        3 = phone number
        4 = website
        5 to 11 = Monday - Sunday
        12 = latitude
        13 = longitude
        14 = information
        15 = distance in miles
        16 = zip code latitude
        17 = zip code longitude
        """
        self.url = None
        self.phone_number = None
        self.map = None
        self.marker = None
        self.midpoint = None
        self.ideal_zoom = None

        self.phone_dialog = MDDialog(
            title="Phone Number",
            text="",
            buttons=[
                MDFlatButton(
                    text="Close",
                    text_color=MDApp.get_running_app().theme_cls.primary_color,
                    on_release=self.close_phone_number_dialog,
                ),
                MDFlatButton(
                    text="Copy",
                    text_color=MDApp.get_running_app().theme_cls.primary_color,
                    on_release=self.copy_phone_number,
                ),
            ],
        )

        self.schedule_data = None

    def on_enter(self, *args):
        self.info = MDApp.get_running_app().row
        self.ids.center_panel.ids.title_box.ids.title.text = self.info[1]
        self.ids.center_panel.ids.list_box.ids.address.text = self.info[2]

        print(
            self.ids.center_panel.ids.buttons_box.ids.call_container.ids.call_button.size
        )

        day = datetime.datetime.today().weekday()
        day_name = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        for index in range(5, 12):
            if self.info[index] is None:
                self.info[index] = "Closed"
        self.ids.center_panel.ids.list_box.ids.hours.text = f"""{day_name[day]}: [color={get_hex_from_color(
            MDApp.get_running_app().theme_cls.primary_color)}]{self.info[day + 5]}[/color]"""

        if self.info[14] is not None:
            self.ids.center_panel.ids.information.text = self.info[14]

        self.ids.center_panel.ids.title_box.ids.distance.text = (
            str(self.info[15]) + " Miles Away"
        )

        # Modify the schedule data table
        # TODO: Make the data table take up the width of the screen
        self.schedule_data = MDDataTable(
            size_hint=(0.9, 0.8),
            column_data=[("Day", dp(20)), ("Hours", dp(35))],
            row_data=[
                ("Monday", self.info[5]),
                ("Tuesday", self.info[6]),
                ("Wednesday", self.info[7]),
                ("Thursday", self.info[8]),
                ("Friday", self.info[9]),
                ("Saturday", self.info[10]),
                ("Sunday", self.info[11]),
            ],
        )
        self.schedule_data.table_data.rows_num = 7
        self.schedule_data.table_data.set_row_data()

        self.map = self.ids.map

        # calculates and sets the view to the midpoint of the foodbank and the person, calculates an ideal zoom value
        self.midpoint = midpoint(
            self.info[12], self.info[13], self.info[16], self.info[17]
        )
        self.map.center_on(self.midpoint[0], self.midpoint[1])
        self.map.zoom = 17
        box = self.map.get_bbox()
        while not (
            box[0] < (self.info[12] and self.info[16]) < box[2]
            and box[1] < (self.info[13] and self.info[17]) < box[3]
        ):
            self.map.zoom -= 1
            box = self.map.get_bbox()
        self.ideal_zoom = self.map.zoom - 1
        self.map.zoom = self.ideal_zoom

        # Adds the foodbank to the map
        self.marker = Marker(
            float(self.info[12]), float(self.info[13]), self.map, self.ideal_zoom
        )
        self.map.add_widget(self.marker)

        # Disables the website button if there is no website
        self.url = self.info[4]
        if self.url is None:
            self.ids.center_panel.ids.buttons_box.ids.website_container.ids.website_button.disabled = (
                True
            )
            self.ids.center_panel.ids.buttons_box.ids.website_container.ids.website_button_text.text_color = (
                MDApp.get_running_app().theme_cls.disabled_hint_text_color
            )
        else:
            self.ids.center_panel.ids.buttons_box.ids.website_container.ids.website_button.disabled = (
                False
            )
            self.ids.center_panel.ids.buttons_box.ids.website_container.ids.website_button_text.text_color = (
                MDApp.get_running_app().theme_cls.primary_color
            )

        # Disables the call button if there is no phone number
        self.phone_number = self.info[3]
        if self.phone_number is None:
            self.ids.center_panel.ids.buttons_box.ids.call_container.ids.call_button.disabled = (
                True
            )
            self.ids.center_panel.ids.buttons_box.ids.call_container.ids.call_button_text.text_color = (
                MDApp.get_running_app().theme_cls.disabled_hint_text_color
            )
        else:
            # Modify the phone dialog
            self.phone_dialog.text = self.info[3]
            self.phone_dialog.size_hint_x = 0.8
            self.phone_dialog.size[1] += 100
            self.ids.center_panel.ids.buttons_box.ids.call_container.ids.call_button.disabled = (
                False
            )
            self.ids.center_panel.ids.buttons_box.ids.call_container.ids.call_button_text.text_color = (
                MDApp.get_running_app().theme_cls.primary_color
            )

        # Set the map size
        Clock.schedule_once(lambda _: self.resize_map())

    def resize_map(self):
        self.ids.map.size = 100, Window.size[1] - self.ids.center_panel.height + 40
        print(f"{self.ids.map.size} is the new size of the map")

    def open_url(self):
        print("opened url")
        webbrowser.open(self.url)

    def call_number(self):
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Intent = autoclass("android.content.Intent")
        Uri = autoclass("android.net.Uri")

        number = Uri.parse(f"tel:{self.info[3].replace('-', '')}")
        intent = Intent(Intent.ACTION_DIAL, number)

        currentActivity = cast("android.app.Activity", PythonActivity.mActivity)
        currentActivity.startActivity(intent)

    def open_google_maps(self):
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Intent = autoclass("android.content.Intent")
        Uri = autoclass("android.net.Uri")

        location = Uri.parse(f'geo:0,0?q={self.info[2].replace(" ", "+")}')
        intent = Intent(Intent.ACTION_VIEW, location)

        currentActivity = cast("android.app.Activity", PythonActivity.mActivity)
        currentActivity.startActivity(intent)

    def open_schedule_data(self):
        self.schedule_data.open()

    def center_on_midpoint(self):
        self.map.center_on(self.midpoint[0], self.midpoint[1])
        self.map.zoom = self.ideal_zoom

    def copy_phone_number(self, _):
        Clipboard.copy(self.info[3])
        Snackbar(text="Copied to Clipboard!").show()

    def close_phone_number_dialog(self, _):
        self.phone_dialog.dismiss()

    def close_schedule_data(self, _):
        self.schedule_data.dismiss()

    def go_back(self):
        self.map.remove_widget(self.marker)
        self.manager.current = "results_screen"


def midpoint(x1, y1, x2, y2):
    # Input values as degrees

    # Convert to radians
    lat1 = math.radians(x1)
    lon1 = math.radians(y1)
    lat2 = math.radians(x2)
    lon2 = math.radians(y2)

    bx = math.cos(lat2) * math.cos(lon2 - lon1)
    by = math.cos(lat2) * math.sin(lon2 - lon1)
    lat3 = math.atan2(
        math.sin(lat1) + math.sin(lat2),
        math.sqrt((math.cos(lat1) + bx) * (math.cos(lat1) + bx) + by ** 2),
    )
    lon3 = lon1 + math.atan2(by, math.cos(lat1) + bx)

    return math.degrees(lat3), math.degrees(lon3)
