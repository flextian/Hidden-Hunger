from kivy.uix.screenmanager import Screen


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zip_code = None

    def go_back(self):
        self.manager.current = 'main_screen'
