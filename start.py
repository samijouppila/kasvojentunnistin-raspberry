# -*- coding: utf-8 -*-

from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.core.window import Window
#Window.fullscreen = True
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

import picamera_face_recognition
import hc04_lukija

class Menu(BoxLayout):
    loginButton = ObjectProperty(None)
    logoutButton = ObjectProperty(None)
    responseLabel = ObjectProperty(None)
    actionStatus = ""

    def initializeMenu(self):
        self.remove_widget(self.responseLabel)

    def mainMenu(self):
        self.remove_widget(self.responseLabel)
        self.add_widget(self.loginButton)
        self.add_widget(self.logoutButton)

    def waitForUserInput(self):
        userrecognized = hc04_lukija.Lukija()
        self.responseLabel.text = "Tunnistetaan..."
        Clock.schedule_once(lambda dt: self.displayUserName(), 0.5)

    def displayUserName(self):
        #username = "käyttäjä"
        username = picamera_face_recognition.recognizeUser()
        if username == "Tunnistamaton käyttäjä":
            self.responseLabel.text = "Käyttäjää ei tunnistettu. \nKirjautuminen ei onnistunut."
        else:
            if self.actionStatus == "login":
                self.responseLabel.text = "Käyttäjä tunnistettu: " + username + "\nSisäänkirjautuminen kirjattu."
            else:
                self.responseLabel.text = "Käyttäjä tunnistettu: " + username + "\nUloskirjautuminen kirjattu."
        Clock.schedule_once(lambda dt: self.mainMenu(), 5)

    def waitingResponse(self):
        self.responseLabel.text = "Heilauta kädellä..."
        self.add_widget(self.responseLabel)
        self.remove_widget(self.loginButton)
        self.remove_widget(self.logoutButton)
        Clock.schedule_once(lambda dt: self.waitForUserInput(), 0.5)

    def startLogin(self):
        self.actionStatus = "login"
        self.waitingResponse()

    def startLogout(self):
        self.actionStatus = "logout"
        self.waitingResponse()

class FaceRecognitionApp(App):
    def build(self):
        Builder.load_file("face-recognition-gui.kv")
        app = Menu()
        app.initializeMenu()
        return app

if __name__ == '__main__':
    FaceRecognitionApp().run()