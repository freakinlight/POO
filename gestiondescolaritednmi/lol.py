from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
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

class Connected(Screen):
    pass

class ConnectedApp(App):
    username = ''
    password = ''
    role = ''

    def build(self):
        manager = ScreenManager()

        manager.add_widget(RoleSelection(name='role_selection'))
        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))  # Add Connected screen

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

if __name__ == '__main__':
    ConnectedApp().run()
