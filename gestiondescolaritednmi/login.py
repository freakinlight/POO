from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        # Set size_hint_x and size_hint_y for the labels and inputs to control size
        self.username_label = Label(text='Username:', size_hint_x=0.3, color=(0, 0, 1, 1))  # Blue color
        self.username_input = TextInput(multiline=False, size_hint_x=0.7, size_hint_y=None, height=30, background_color=(0.9, 0.9, 0.9, 1))  # Light gray background

        self.password_label = Label(text='Password:', size_hint_x=0.3, color=(0, 0, 1, 1))  # Blue color
        self.password_input = TextInput(multiline=False, password=True, size_hint_x=0.7, size_hint_y=None, height=30, background_color=(0.9, 0.9, 0.9, 1))  # Light gray background

        self.login_button = Button(text='Login', on_press=self.check_credentials, background_color=(0, 0.7, 0, 1))  # Green color
        self.exit_button = Button(text='Exit', on_press=self.exit_app, background_color=(1, 0, 0, 1))  # Red color

        self.add_widget(self.username_label)
        self.add_widget(self.username_input)
        self.add_widget(self.password_label)
        self.add_widget(self.password_input)
        self.add_widget(self.login_button)
        self.add_widget(self.exit_button)

    def check_credentials(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        # Here you would typically perform authentication logic.
        # For simplicity, let's just print the entered credentials.
        print(f"Username: {username}, Password: {password}")

    def exit_app(self, instance):
        App.get_running_app().stop()


class LoginApp(App):
    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    LoginApp().run()
