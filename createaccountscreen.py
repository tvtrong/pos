from kivy.uix.screenmanager import Screen
import json
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import requests


class CreateAccountScreen(Screen):
    def __init__(self, **kwargs):
        super(CreateAccountScreen, self).__init__(**kwargs)
        self.url = "https://loginkivy.firebaseio.com/.json"
        self.auth = '4TAsuXNTgJJ9QFfddMvCMpnXz3zrmgyubY0v1a3l'
        self.dialog = MDDialog()

    def close_username_dialog(self, obj):
        self.dialog.dismiss()

    def signup(self):
        signupEmail = self.ids.signup_email.text
        signupPassword = self.ids.signup_password.text
        signupUsername = self.ids.signup_username.text
        if signupEmail == '' or signupPassword == '' or signupUsername == '':
            cancel_btn_username_dialogue = MDFlatButton(
                text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Input', text='All fields Required', size_hint=(
                0.7, 0.2), buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        elif len(signupUsername.split()) > 1:
            cancel_btn_username_dialogue = MDFlatButton(
                text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Username', text='Please enter username without space', size_hint=(
                0.7, 0.2), buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            signup_info = str(
                {f'\"{signupEmail}\":{{"Password":\"{signupPassword}\","Username":\"{signupUsername}\"}}'})
            signup_info = signup_info.replace(".", "-")
            signup_info = signup_info.replace("\'", "")
            to_database = json.loads(signup_info)
            try:
                requests.patch(url=self.url, json=to_database)
                self.change_screen('sign_in_screen')
            except Exception.message as err:
                cancel_btn_username_dialogue = MDFlatButton(
                    text='Close', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Error', text=err, size_hint=(
                    0.7, 0.2), buttons=[cancel_btn_username_dialogue])
                self.dialog.open()

    def change_screen(self, scrn):
        self.parent.parent.ids['screen_manager'].current = scrn
