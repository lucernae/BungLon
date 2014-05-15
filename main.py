import kivy
kivy.require('1.8.0')
from kivy.app import App
from bunglon.screen.mainmenu import MainMenuScreen
from kivy.uix.screenmanager import SlideTransition, ScreenManager


class MainApp(App):

    def build(self):
        self.cur_screen = MainMenuScreen()
        self.transition = SlideTransition(duration=0.35)
        root = ScreenManager(transition=self.transition)
        root.switch_to(self.cur_screen)
        return root



if __name__ == '__main__':
    MainApp().run()