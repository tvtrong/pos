from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivymd.uix.picker import MDThemePicker,MDDatePicker
from datetime import datetime
from pymongo import MongoClient
import hashlib
from kivy.clock import Clock
from kivymd.uix.label import Label
from kivy.uix.modalview import ModalView
import requests


class Notify(ModalView):
    def __init__(self, **kwargs):
        super(Notify, self).__init__(**kwargs)

        self.size_hint = (None, None)
        self.background_color = (108/255, 90/255, 90/255, .76)
        self.size = (270, 50)


class SignInScreen(Screen):
    def __init__(self, **kwargs):
        super(SignInScreen, self).__init__(**kwargs)
        self.notify = Notify()
        self.url = "https://loginkivy.firebaseio.com/.json"
        self.auth = '4TAsuXNTgJJ9QFfddMvCMpnXz3zrmgyubY0v1a3l'
        self.login_check = False

    def change_screen(self, scrn):
        self.parent.parent.ids['screen_manager'].current = scrn

    def animate_card(self, widget):
        anim = Animation(pos_hint={'center_y': .43}, duration=1)
        anim.start(widget)

    def animate_background(self, widget):
        anim = Animation(size_hint_y=1) + Animation(size_hint_y=.5)
        anim.start(widget.ids.bx)

    def get_date(self, date):
        '''
        :type date: <class 'datetime.date'>
        '''

    def show_date_picker(self):
        min_date = datetime.strptime("2020:02:15", '%Y:%m:%d').date()
        max_date = datetime.strptime("2090:02:20", '%Y:%m:%d').date()
        date_dialog = MDDatePicker(
            callback=self.get_date,
            min_date=min_date,
            max_date=max_date,
        )
        date_dialog.open()

    def show_theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()

    def cb(self, dt):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def login(self):
        loginEmail = self.ids.username_field.text
        loginPassword = self.ids.pwd_field.text

        self.login_check = False
        supported_loginEmail = loginEmail.replace('.', '-')
        supported_loginPassword = loginPassword.replace('.', '-')
        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        emails = set()
        for key, value in data.items():
            emails.add(key)
        if supported_loginEmail in emails and supported_loginPassword == data[supported_loginEmail]['Password']:
            self.username = data[supported_loginEmail]['Username']
            self.email = supported_loginEmail.replace('-', '.')
            self.login_check = True
            self.change_screen('dashboard_screen')
        else:
            self.notify.add_widget(
                Label(text='[color=#FF0000][b]Invalid Email or Password[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.cb, 1.1)

    def username_changer(self):
        if self.login_check:
            self.parent.parent.ids.dashboard_screen.ids.toolbar.title = f"Welcome {self.username}"
            self.parent.parent.ids.dashboard_screen.ids.nv.ids.u_name.text = str(self.username)
            self.parent.parent.ids.dashboard_screen.ids.nv.ids.u_email.text = str(self.email)

    def validate_user(self):
        client = MongoClient()
        db = client.silverpos
        users = db.users

        user = self.ids['username_field']
        pwd = self.ids['pwd_field']

        uname = user.text
        passw = pwd.text

        if not uname and not passw:
            self.notify.add_widget(
                Label(text='[color=#FFFFFF][b]Username and Password are Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.cb, 1.1)
        elif not uname:
            self.notify.add_widget(
                Label(text='[color=#FFFFFF][b]Username is Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.cb, 1.1)
            # info.text = "[color=#FF0000]Username required ![/color]"
        elif passw == '':
            self.notify.add_widget(
                Label(text='[color=#FFFFFF][b]Password is Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.cb, 1.1)
            # info.text = "[color=#FF0000]Password required ![/color]"
        else:
            user = users.find_one(({'user_name': uname}))
            if user == None:
                self.notify.add_widget(
                    Label(text='[color=#FF0000][b]Invalid Username[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.cb, 1.1)
            # info.text = "[color=#FF0000]Invalid Username ![/color]"
            else:
                passw = hashlib.sha256(passw.encode()).hexdigest()
                if passw == user['password']:
                    des = user['designation']
                    self.notify.add_widget(
                        Label(text='[color=#00FF00][b]Success Login[/b][/color]', markup=True))
                    self.notify.open()
                    Clock.schedule_once(self.cb, 1.3)
                    self.change_screen('dashboard_screen')

                    # self.parent.parent.parent.ids.scrn_op.children[0].ids.loggedin_user.text = uname
                    # if des == 'Administrator':
                    #     self.parent.parent.current = 'scrn_admin'
                    # else:
                    #     self.parent.parent.current = 'scrn_op'
                else:
                    self.notify.add_widget(
                        Label(text='[color=#FF0000][b]Invalid Password[/b][/color]', markup=True))
                    self.notify.open()
                    Clock.schedule_once(self.cb, 1.1)
