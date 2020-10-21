from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.animation import Animation
from pymongo import MongoClient
import hashlib
from kivy.clock import Clock
from kivymd.uix.label import Label
from kivy.uix.modalview import ModalView
from kivymd.uix.picker import MDThemePicker,MDDatePicker
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
Builder.load_file('login/login.kv')


class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.notify = Notify()

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

    def animate_card(self, widget):
        anim = Animation(pos_hint={'center_y': .6}, duration=1.5)
        anim.start(widget)

    def animate_background(self, widget):
        anim = Animation(size_hint_y=1) + Animation(size_hint_y=.5)
        anim.start(widget.ids.bx)

    def cb(self, dt):
        self.notify.dismiss()
        self.notify.clear_widgets()

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


class Notify(ModalView):
    def __init__(self, **kwargs):
        super(Notify, self).__init__(**kwargs)

        self.size_hint = (None, None)
        self.background_color = (108/255, 90/255, 90/255, .76)
        self.size = (270, 50)


class LoginApp(MDApp):
    def __init__(self, **kwargs):
        super(LoginApp, self).__init__(**kwargs)

    def build(self):
        self.title = 'Login'
        return LoginScreen()


if __name__ == '__main__':
    LoginApp().run()
