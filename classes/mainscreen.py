import os

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
