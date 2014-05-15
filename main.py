import kivy
from bunglon.screen.gamescreen import GameScreen

kivy.require('1.8.0')
from kivy.app import App
from bunglon.screen.mainmenu import MainMenuScreen
from kivy.uix.screenmanager import SlideTransition, ScreenManager


class MainApp(App):

    def build(self):
        root = ScreenManager(transition=SlideTransition(duration=0.35))
        root.add_widget(MainMenuScreen())
        root.add_widget(GameScreen())
        return root


if __name__ == '__main__':
    MainApp().run()