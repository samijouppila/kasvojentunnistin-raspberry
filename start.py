# -*- coding: utf-8 -*-

from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.core.window import Window
Window.fullscreen = True
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

import datetime
import picamera_face_recognition
import hc04_lukija
import upload_to_dropbox
import database_request


class Menu(BoxLayout):
    loginButton = ObjectProperty(None)
    logoutButton = ObjectProperty(None)
    responseLabel = ObjectProperty(None)
    actionStatus = ""
    currentImageName = ""

    def initializeMenu(self):
        self.remove_widget(self.responseLabel)

    def nextImageIndex(self):
        return database_request.receiveLatestIndex() + 1

    def mainMenu(self):
        self.remove_widget(self.responseLabel)
        self.add_widget(self.loginButton)
        self.add_widget(self.logoutButton)

    def sendEventToDatabase(self, username):
        now = datetime.datetime.now()
        if username == "Tunnistamaton käyttäjä":
            database_request.sendNewReport(username, "ei tunnistettu", str(now), self.currentImageName)
            self.responseLabel.text = "Kirjautuminen ei onnistunut."
        else:
            if self.actionStatus == "login":
                self.responseLabel.text = "Sisäänkirjautuminen kirjattu."
                database_request.sendNewReport(username, "sisään", str(now), self.currentImageName)
            else:
                self.responseLabel.text = "Uloskirjautuminen kirjattu."
                database_request.sendNewReport(username, "ulos", str(now), self.currentImageName)
        Clock.schedule_once(lambda dt: self.mainMenu(), 5)

    def uploadToDropbox(self, username):
        upload_to_dropbox.startDropboxUpload(self.currentImageName)
        Clock.schedule_once(lambda dt: self.sendEventToDatabase(username), 0.5)


    def displayUserName(self):
        #username = "käyttäjä"
        self.currentImageName = "kuva" + str(self.nextImageIndex()) + ".jpg"
        username = picamera_face_recognition.recognizeUser(self.currentImageName)
        if username == "Tunnistamaton käyttäjä":
            self.responseLabel.text = "Käyttäjää ei tunnistettu."
        else:
            self.responseLabel.text = "Käyttäjä tunnistettu: " + username
        Clock.schedule_once(lambda dt: self.uploadToDropbox(username), 0.5)

    def waitForUserInput(self):
        userrecognized = hc04_lukija.Lukija()
        self.responseLabel.text = "Tunnistetaan..."
        Clock.schedule_once(lambda dt: self.displayUserName(), 0.5)

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