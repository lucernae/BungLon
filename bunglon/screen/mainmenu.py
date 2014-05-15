from bunglon.screen.gamescreen import GameScreen
from kivy.uix.screenmanager import Screen, SlideTransition


class MainMenuScreen(Screen):

    def play_normal(self, event):
        screen = self.manager.get_screen('game screen')
        screen.play_normal()
        screen.bind(on_enter=screen.init_screen)
        self.manager.transition = SlideTransition(duration=0.35)
        self.manager.current = 'game screen'

    def play_blind(self, event):
        screen = self.manager.get_screen('game screen')
        screen.play_blind()
        screen.bind(on_enter=screen.init_screen)
        self.manager.transition = SlideTransition(duration=0.35)
        self.manager.current = 'game screen'