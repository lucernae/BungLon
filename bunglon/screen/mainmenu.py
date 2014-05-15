from bunglon.screen.gamescreen import GameScreen
from kivy.uix.screenmanager import Screen


class MainMenuScreen(Screen):

    def on_touch_down(self, touch):
        self.manager.switch_to(GameScreen())

