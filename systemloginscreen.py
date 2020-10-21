from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import os.path
import progressspinner


folder = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(folder + "/themedwidgets.kv")
Builder.load_file(folder + "/loadingpopup.kv")
Builder.load_file(folder + "/signinscreen.kv")
Builder.load_file(folder + "/welcomescreen.kv")
Builder.load_file(folder + "/createaccountscreen.kv")
Builder.load_file(folder + "/dashboardscreen.kv")

from welcomescreen import WelcomeScreen
from signinscreen import SignInScreen
from createaccountscreen import CreateAccountScreen
from dashboardscreen import MainDashboardScreen


class SystemLoginScreen(Screen):
    pass