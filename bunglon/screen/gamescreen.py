from cmath import sqrt
import kivy
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, FadeTransition, FallOutTransition, SlideTransition
from random import randint
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty
from bunglon import colorlist as cl

kivy.require('1.8.0')


class GameScreen(Screen):

    target_score = NumericProperty(0)
    num_question = NumericProperty(0)
    max_question = NumericProperty(0)
    question_id = NumericProperty(0)
    color_entry = ObjectProperty()
    cur_score = NumericProperty(0)
    is_normal_mode = BooleanProperty()
    is_blind_mode = BooleanProperty()

    @staticmethod
    def invert_color(color):
        return Color(1.0 - color.r, 1.0 - color.g, 1.0 - color.b, color.a)

    def play_normal(self):
        self.is_normal_mode = True
        self.is_blind_mode = False

    def play_blind(self):
        self.is_blind_mode = True
        self.is_normal_mode = False

    def init_screen(self, event=None):
        # reset binding
        self.guess_button.unbind(on_press=self.create_question)
        self.guess_button.unbind(on_press=self.answer_question)
        # reset number of question
        self.cur_score = 0
        self.target_score = 0
        self.increment_score()
        self.num_question = 0
        self.max_question = 10
        # create question
        self.create_question()

    def back_to_main(self, event):
        self.manager.transition = SlideTransition(direction='right', duration=0.35)
        self.manager.current = self.manager.previous()

    def create_question(self, event=None):
        if self.num_question < self.max_question:
            self.num_question += 1
            self.question_id = randint(0, len(cl.colorlist) - 1)
            self.color_entry = cl.colorlist[self.question_id]
            self.color_text.text = self.color_entry[0]
            self.guess_button.text = "Guess"
            self.guess_button.unbind(on_press=self.create_question)
            self.guess_button.bind(on_press=self.answer_question)
            # clear preview color
            if self.is_blind_mode:
                with self.color_guess.canvas.before:
                    Color(1, 1, 1)
                    Rectangle(pos=self.color_guess.pos, size=self.color_guess.size)
                self.color_guess.color = [0, 0, 0, 1]
            else:
                with self.color_guess.canvas.before:
                    Color(0, 0, 0)
                    Rectangle(pos=self.color_guess.pos, size=self.color_guess.size)
                self.color_guess.color = [1, 1, 1, 1]

            if self.is_normal_mode:
                color = Color(self.color_entry[1] / 255.0, self.color_entry[2] / 255.0, self.color_entry[3] / 255.0)
                with self.color_answer.canvas.before:
                    Color(self.color_entry[1] / 255.0, self.color_entry[2] / 255.0, self.color_entry[3] / 255.0)
                    Rectangle(pos=self.color_answer.pos, size=self.color_answer.size)
                self.color_answer.color = [1.0 - color.r, 1.0 - color.g, 1.0 - color.b, color.a]
            else:
                with self.color_answer.canvas.before:
                    Color(0, 0, 0)
                    Rectangle(pos=self.color_answer.pos, size=self.color_answer.size)
        else:
            self.guess_button.text = "Game Over. Restart?"
            self.guess_button.unbind(on_press=self.create_question)
            self.init_screen()

    def answer_question(self, event):
        print 'answer'
        red = (self.red_slider.value - self.color_entry[1]) / 255.0
        green = (self.green_slider.value - self.color_entry[2]) / 255.0
        blue = (self.blue_slider.value - self.color_entry[3]) / 255.0
        # calculate distance from answer value
        distance = sqrt(red**2 + green**2 + blue**2)
        max_distance = sqrt(3)
        # calculate score
        score = (max_distance - distance) * sqrt(3) * 1000 / 3
        self.target_score += int(score.real if score.real > 0 else 0)
        # schedule score increment
        Clock.schedule_interval(self.increment_score, 1.0/60)
        # show answer color and guess color
        with self.color_guess.canvas.before:
            Color(self.red_slider.value / 255.0, self.green_slider.value / 255.0, self.blue_slider.value / 255.0)
            Rectangle(pos=self.color_guess.pos, size=self.color_guess.size)

        with self.color_answer.canvas.before:
            Color(self.color_entry[1] / 255.0, self.color_entry[2] / 255.0, self.color_entry[3] / 255.0)
            Rectangle(pos=self.color_answer.pos, size=self.color_answer.size)

        # change answer button to next question
        self.guess_button.text = 'Next Question'
        self.guess_button.unbind(on_press=self.answer_question)
        self.guess_button.bind(on_press=self.create_question)

    def increment_score(self, event=None):
        if self.cur_score < self.target_score:
            self.cur_score += 10
        else:
            self.cur_score = self.target_score
            Clock.unschedule(self.increment_score)
        self.score_text.text = \
            "score : {} \n {} question left".format(self.cur_score, self.max_question - self.num_question)

    def preview_color(self, touch):
        red = self.red_slider.value
        green = self.green_slider.value
        blue = self.blue_slider.value

        with self.red_preview.canvas:
            Color(red / 255.0, 0, 0)
            Rectangle(pos=self.red_preview.pos, size=self.red_preview.size)

        with self.green_preview.canvas:
            Color(0, green / 255.0, 0)
            Rectangle(pos=self.green_preview.pos, size=self.green_preview.size)

        with self.blue_preview.canvas:
            Color(0, 0, blue / 255.0)
            Rectangle(pos=self.blue_preview.pos, size=self.blue_preview.size)

        if self.is_blind_mode:
            color = \
                Color(self.red_slider.value / 255.0, self.green_slider.value / 255.0, self.blue_slider.value / 255.0)
            self.color_guess.color = [1.0 - color.r, 1.0 - color.g, 1.0 - color.b, color.a]
            with self.color_guess.canvas.before:
                Color(self.red_slider.value / 255.0, self.green_slider.value / 255.0, self.blue_slider.value / 255.0)
                Rectangle(pos=self.color_guess.pos, size=self.color_guess.size)