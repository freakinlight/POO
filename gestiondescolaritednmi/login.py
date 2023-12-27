import hashlib
import json
import os

import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os


class RoleSelection(Screen):
    def __init__(self, **kwargs):
        super(RoleSelection, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        role_labels = ['Teacher', 'Student', 'Administrator']

        for role in role_labels:
            btn = Button(text=role, size_hint=(None, None), width=200, height=50)
            btn.bind(on_release=lambda instance, r=role: self.on_role_selected(r))
            layout.add_widget(btn)

        self.add_widget(layout)

    def on_role_selected(self, role):
        app = App.get_running_app()
        app.role = role

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'login'

class Login(Screen):
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        # Assuming you want to use the role in the login screen as well
        app.role  # Use app.role as needed

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'

        app.config.read(app.get_application_config())
        app.config.write()

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

class ConnectedApp(App):
    username = ''
    password = ''
    role = ''

    def build(self):
        manager = ScreenManager()

        manager.add_widget(RoleSelection(name='role_selection'))
        manager.add_widget(Login(name='login'))

        return manager

    def get_application_config(self):
        if not self.username:
            return super(ConnectedApp, self).get_application_config()

        conf_directory = os.path.join(self.user_data_dir, self.username)

        if not os.path.exists(conf_directory):
            os.makedirs(conf_directory)

        return super(ConnectedApp, self).get_application_config(
            os.path.join(conf_directory, 'config.cfg')
        )


def blake2b(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

class LoginCredentials:
    DEFAULT_LOGINS = [{'username': 'admin', 'password': blake2b('admin')}]

    def __init__(self, path='credentials.json'):
        self.path = path
        if not os.path.exists(path):
            with open(self.path, 'w+') as f:
                json.dump(self.DEFAULT_LOGINS, f)

    def read(self):
        with open(self.path, 'r') as f:
            return json.load(f)
    
    def write(self, data):
        with open(self.path, 'w') as f:
            json.dump(data, f)

    def validate(self, username, password):
        for pair in self.read():
            if pair['username'] == username and pair['password'] == blake2b(password):
                return True
            
        return False

class LoginLayout(FloatLayout):
    INPUT_HEIGHT = 50

    def __init__(self, **kwargs):
        super(LoginLayout, self).__init__(**kwargs)

        # Container for centering content
        container = BoxLayout(orientation='vertical', size_hint=(None, None), width=300, height=200)
        container.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        container.spacing = 15

        # Username field
        container.add_widget(Label(text='Username', size_hint=(1, None), height=30))
        self.username = TextInput(multiline=False, size_hint=(1, None), height=self.INPUT_HEIGHT, padding=10)
        container.add_widget(self.username)

        # Password field
        container.add_widget(Label(text='Password', size_hint=(1, None), height=30))
        self.password = TextInput(password=True, multiline=False, size_hint=(1, None), height=self.INPUT_HEIGHT)
        container.add_widget(self.password)

        # Login button
        self.login_btn = Button(text='Login', size_hint=(1, None), height=self.INPUT_HEIGHT)
        self.login_btn.bind(on_press=self.validate_credentials)
        container.add_widget(self.login_btn)

        self.message = Label(text='', size_hint=(1, None), height=30)
        container.add_widget(self.message)

        # Add the container to the main layout
        self.add_widget(container)

        # Add credentials manager
        self.credentials = LoginCredentials()

    def validate_credentials(self, _):
        username = self.username.text
        password = self.password.text
        if self.credentials.validate(username, password):
            self.parent.manager.transition = SlideTransition(direction='left')
            self.parent.manager.current = 'main'
            self.message.text = ''
        else:
            self.message.text = 'Invalid credentials'

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.add_widget(LoginLayout())

class MainLayout(FloatLayout):
    INPUT_HEIGHT = 50

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        # Container for centering content
        container = BoxLayout(orientation='vertical', size_hint=(None, None), width=300, height=200)
        container.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        container.spacing = 15

        container.add_widget(Label(text='Logged in successfully', size_hint=(1, None), height=70))

        # Login button
        self.logout_btn = Button(text='Logout', size_hint=(1, None), height=self.INPUT_HEIGHT)
        self.logout_btn.bind(on_press=self.logout)
        container.add_widget(self.logout_btn)

        # Add the container to the main layout
        self.add_widget(container)

    def logout(self, _):
        self.parent.manager.transition = SlideTransition(direction='right')
        self.parent.manager.current = 'login'
    
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.add_widget(MainLayout())

class PGSScreenManager(ScreenManager):
    pass

class PGSApp(App):
    def build(self):
        sm = PGSScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    PGSApp().run()