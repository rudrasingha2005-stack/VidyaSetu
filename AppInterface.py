from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
import cv2
import datetime
import random

KV = """
ScreenManager:
    LoginScreen:
    MainScreen:
    MiddayMealScreen:
    CameraScreen:
    AttendanceRecordScreen:

<LoginScreen>:
    name: "login"

    MDFloatLayout:
        MDLabel:
            text: "📚 School Attendance"
            halign: "center"
            font_style: "H5"
            pos_hint: {"center_y": .9}

        MDTextField:
            id: username
            hint_text: "Username"
            pos_hint: {"center_x": .5, "center_y": .7}
            size_hint_x: .8

        MDTextField:
            id: password
            hint_text: "Password"
            password: True
            pos_hint: {"center_x": .5, "center_y": .6}
            size_hint_x: .8

        MDRaisedButton:
            text: "Login"
            md_bg_color: app.theme_cls.primary_color
            pos_hint: {"center_x": .5, "center_y": .48}
            on_release: app.check_login(username.text, password.text)

        MDTextButton:
            text: "Login as Admin"
            pos_hint: {"center_x": .5, "center_y": .42}
            on_release: app.quick_admin_login()

<MainScreen>:
    name: "main"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Attendance App"
            left_action_items: [["account", lambda x: None]]
            right_action_items: [["logout", lambda x: app.logout()]]

        MDLabel:
            id: role_label
            text: "Welcome!"
            halign: "center"
            font_style: "H6"
            size_hint_y: .2

        MDGridLayout:
            cols: 1
            spacing: "15dp"
            padding: "20dp"
            adaptive_height: True

            MDRaisedButton:
                text: "📌 Mark Attendance"
                md_bg_color: 0, 0.6, 1, 1
                on_release: app.open_camera()

            MDRaisedButton:
                text: "📊 Records / Analytics"
                md_bg_color: 1, 0.5, 0, 1
                on_release: app.open_attendance_record()

            MDRaisedButton:
                text: "📝 Student Profile"
                md_bg_color: 0.6, 0, 0.8, 1

            MDRaisedButton:
                text: "🍽️ Midday Meal Scheme"
                md_bg_color: 0.2, 0.7, 0.2, 1
                on_release: app.open_midday_meal()

<MiddayMealScreen>:
    name: "midday"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Midday Meal Scheme"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]

        MDLabel:
            text: "🔒 Restricted access for school administration"
            halign: "center"
            theme_text_color: "Error"
            font_style: "H6"

<CameraScreen>:
    name: "camera"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Face Scan Attendance"
            left_action_items: [["arrow-left", lambda x: app.close_camera()]]

        Image:
            id: camera_view
            allow_stretch: True
            keep_ratio: True

        MDRaisedButton:
            text: "✅ Capture Attendance"
            md_bg_color: 0, 0.7, 0.2, 1
            pos_hint: {"center_x": .5}
            on_release: app.capture_attendance()

<AttendanceRecordScreen>:
    name: "attendance_record"

    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "20dp"

        MDTopAppBar:
            title: "Attendance Records"
            left_action_items: [["arrow-left", lambda x: app.go_back()]]

        MDLabel:
            text: "Welcome to the Student Attendance Record Page"
            halign: "center"
            font_style: "H5"
"""


class LoginScreen(Screen): pass


class MainScreen(Screen): pass


class MiddayMealScreen(Screen): pass


class CameraScreen(Screen): pass


class AttendanceRecordScreen(Screen): pass


class AttendanceApp(MDApp):
    role = "Student"

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.cap = None
        self.event = None
        return Builder.load_string(KV)

    # -------------------- LOGIN -------------------- #
    def check_login(self, username, password):
        if username == "user1" and password == "pass1":
            self.set_role("Student")
            self.root.current = "main"
        elif username == "admin" and password == "admin":
            self.set_role("Admin")
            self.root.current = "main"
        else:
            self.show_dialog("Login Failed", "Invalid Username or Password")

    def quick_admin_login(self):
        self.set_role("Admin")
        self.root.current = "main"

    def set_role(self, role):
        self.role = role
        self.root.get_screen("main").ids.role_label.text = f"Welcome, {role}!"

    def logout(self):
        self.role = "Student"
        login_screen = self.root.get_screen("login")
        login_screen.ids.username.text = ""
        login_screen.ids.password.text = ""
        self.root.current = "login"

    # -------------------- MIDDAY MEAL -------------------- #
    def open_midday_meal(self):
        if self.role == "Admin":
            self.root.current = "midday"
        else:
            self.show_dialog("Access Denied", "Only school administration can access the Midday Meal Scheme.")

    def go_back(self):
        self.root.current = "main"

    # -------------------- CAMERA -------------------- #
    def open_camera(self):
        self.root.current = "camera"
        self.cap = cv2.VideoCapture(0)
        self.event = Clock.schedule_interval(self.update_camera, 1.0 / 30.0)

    def update_camera(self, dt):
        # ret, frame = self.cap.read()
        # if ret:
        #     buf = cv2.flip(frame, 1).tobytes()
        #     texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        #     texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        #     self.root.get_screen("camera").ids.camera_view.texture = texture
            ret, frame = self.cap.read()
            if ret:
                # Flip vertically and horizontally to correct orientation
                frame = cv2.flip(frame, -1)  # -1 flips both axes
                buf = frame.tobytes()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.root.get_screen("camera").ids.camera_view.texture = texture

    def capture_attendance(self):
        self.last_attendance = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.show_dialog("✅ Attendance", "Attendance Recorded Successfully!")
        self.close_camera()

    def close_camera(self):
        if self.cap:
            self.cap.release()
        if self.event:
            Clock.unschedule(self.event)
        self.root.current = "main"

    # -------------------- ATTENDANCE RECORD -------------------- #
    def open_attendance_record(self):
        self.root.current = "attendance_record"

    # -------------------- UTILS -------------------- #
    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDRectangleFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()


AttendanceApp().run()
