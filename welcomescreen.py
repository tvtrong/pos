from kivy.uix.screenmanager import Screen
import sys


class WelcomeScreen(Screen):
    def stop(self):
        sys.exit()
