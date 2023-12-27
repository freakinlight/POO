import hashlib
import json
import os

import kivy

kivy.require("2.1.0")  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup


def blake2b(password):
    return hashlib.blake2b(password.encode("utf-8")).hexdigest()


class LoginCredentials:
    DEFAULT_LOGINS = [
        {"username": "admin", "password": blake2b("admin"), "type": "administrator"}
    ]

    def __init__(self, path="credentials.json"):
        self.path = path
        if not os.path.exists(path):
            with open(self.path, "w+") as f:
                json.dump(self.DEFAULT_LOGINS, f)

    def read(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def write(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f)

    def validate(self, username, password):
        for pair in self.read():
            if pair["username"] == username and pair["password"] == blake2b(password):
                return True

        return False

    def is_admin(self, username):
        for pair in self.read():
            if pair["username"] == username and pair["type"] == "administrator":
                return True
        return False


CREDENTIALS = LoginCredentials()


class AdminManagementLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(AdminManagementLayout, self).__init__(**kwargs)
        self.orientation = "vertical"

        # Interface components
        self.add_widget(Label(text="Admin Management Screen"))

        # Buttons for actions
        self.add_button("Add Teacher", self.add_teacher)
        self.add_button("Add Student", self.add_student)
        self.add_button("Remove User", self.remove_user)
        self.add_button("Search User", self.search_user)

    def add_button(self, text, on_press_func):
        button = Button(text=text, size_hint=(1, None), height=50)
        button.bind(on_press=on_press_func)
        self.add_widget(button)

    def add_teacher(self, _):
        self.show_popup("Add Teacher", self.save_teacher)

    def add_student(self, _):
        self.show_popup("Add Student", self.save_student)

    def remove_user(self, _):
        self.show_popup("Remove User", self.remove_user_callback)

    def search_user(self, _):
        self.show_popup("Search User", self.search_user_callback)

    def show_popup(self, title, callback_func):
        content = GridLayout(cols=2, spacing=10, size_hint_y=None, height=150)
        content.add_widget(Label(text="Username:"))
        username_input = TextInput()
        content.add_widget(username_input)
        content.add_widget(Label(text="Password:"))
        password_input = TextInput(password=True)
        content.add_widget(password_input)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(400, 200),
            auto_dismiss=False,
        )

        def on_submit(_):
            callback_func(username_input.text, password_input.text)
            popup.dismiss()

        submit_button = Button(text="Submit")
        submit_button.bind(on_press=on_submit)
        content.add_widget(submit_button)

        popup.open()

    def save_student(self, username, password):
        # Logic for saving the user to credentials.json
        new_user = {
            "username": username,
            "password": blake2b(password),
            "type": "student",
        }
        credentials_data = CREDENTIALS.read()
        credentials_data.append(new_user)
        CREDENTIALS.write(credentials_data)

    def save_teacher(self, username, password):
        # Logic for saving the user to credentials.json
        new_user = {
            "username": username,
            "password": blake2b(password),
            "type": "teacher",
        }
        credentials_data = CREDENTIALS.read()
        credentials_data.append(new_user)
        CREDENTIALS.write(credentials_data)

    def remove_user_callback(self, username, password):
        # Logic for removing the user from credentials.json
        credentials_data = CREDENTIALS.read()
        credentials_data = [
            user for user in credentials_data if user["username"] != username
        ]
        CREDENTIALS.write(credentials_data)

    def search_user_callback(self, username, password):
        # Logic for searching for the user in credentials.json
        user_found = [
            user for user in CREDENTIALS.read() if user["username"] == username
        ]
        if user_found:
            print(f"User found: {user_found[0]}")
        else:
            print("User not found")


class AdminManagementScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminManagementScreen, self).__init__(**kwargs)
        self.add_widget(AdminManagementLayout())


class LoginLayout(FloatLayout):
    INPUT_HEIGHT = 50

    def __init__(self, **kwargs):
        super(LoginLayout, self).__init__(**kwargs)

        # Container for centering content
        container = BoxLayout(
            orientation="vertical", size_hint=(None, None), width=300, height=200
        )
        container.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        container.spacing = 15

        # Username field
        container.add_widget(Label(text="Username", size_hint=(1, None), height=30))
        self.username = TextInput(
            multiline=False, size_hint=(1, None), height=self.INPUT_HEIGHT, padding=10
        )
        container.add_widget(self.username)

        # Password field
        container.add_widget(Label(text="Password", size_hint=(1, None), height=30))
        self.password = TextInput(
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=self.INPUT_HEIGHT,
        )
        container.add_widget(self.password)

        # Login button
        self.login_btn = Button(
            text="Login", size_hint=(1, None), height=self.INPUT_HEIGHT
        )
        self.login_btn.bind(on_press=self.validate_credentials)
        container.add_widget(self.login_btn)

        self.message = Label(text="", size_hint=(1, None), height=30)
        container.add_widget(self.message)

        # Add the container to the main layout
        self.add_widget(container)

        # Add credentials manager
        # self.credentials = LoginCredentials()

    def validate_credentials(self, _):
        username = self.username.text
        password = self.password.text
        if CREDENTIALS.validate(username, password):
            if CREDENTIALS.is_admin(username):
                self.parent.manager.transition = SlideTransition(direction="left")
                self.parent.manager.current = "admin_management"
            else:
                self.parent.manager.transition = SlideTransition(direction="left")
                self.parent.manager.current = "main"
            self.message.text = ""
        else:
            self.message.text = "Invalid credentials"


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.add_widget(LoginLayout())


class MainLayout(FloatLayout):
    INPUT_HEIGHT = 50

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        # Container for centering content
        container = BoxLayout(
            orientation="vertical", size_hint=(None, None), width=300, height=200
        )
        container.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        container.spacing = 15

        container.add_widget(
            Label(text="Logged in successfully", size_hint=(1, None), height=70)
        )

        # Logout button
        self.logout_btn = Button(
            text="Logout", size_hint=(1, None), height=self.INPUT_HEIGHT
        )
        self.logout_btn.bind(on_press=self.logout)
        container.add_widget(self.logout_btn)

    

        # Add the container to the main layout
        self.add_widget(container)

    def logout(self, _):
        self.parent.manager.transition = SlideTransition(direction="right")
        self.parent.manager.current = "login"

    def go_to_admin_management(self, _):
        self.parent.manager.transition = SlideTransition(direction="up")
        self.parent.manager.current = "admin_management"


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.add_widget(MainLayout())


class PGSScreenManager(ScreenManager):
    pass


class PGSApp(App):
    def build(self):
        sm = PGSScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(AdminManagementScreen(name="admin_management"))
        return sm


if __name__ == "__main__":
    PGSApp().run()
