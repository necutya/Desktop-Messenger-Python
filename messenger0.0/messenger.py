import threading
import time
from datetime import datetime

from PyQt5 import QtWidgets
import clientui
import requests


class MessengerApp(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button_cliked)
        threading.Thread(target=self.update_messages).start()

    def send_message(self, username, password, text):
        response = requests.post(
            "http://127.0.0.1:5000/auth",
            json={"username": username, "password": password}
        )
        if not response.json()['ok']:
            self.add_to_chat("ERROR: Unauthorized user!")
            return

        response = requests.post(
            "http://127.0.0.1:5000/send",
            json={"username": username, "password": password, "text": text}
        )
        if not response.json()['ok']:
            self.add_to_chat("ERROR: Message was not send!")

    def button_cliked(self):
        try:
            self.send_message(
                self.textEdit_2.toPlainText(),  # username
                self.textEdit_3.toPlainText(),  # password
                self.textEdit.toPlainText()  # text
            )
        except:
            self.add_to_chat("ERROR!")
        self.textEdit.setText('')

    def add_to_chat(self, text):
        self.textBrowser.append(text)

    def update_messages(self):
        last_time = 0
        while True:
            try:
                response = requests.get("http://127.0.0.1:5000/messages", params={'after': last_time})
                messages = response.json()["messages"]

                for message in messages:
                    self.add_to_chat(message["username"] + ' ' +
                                     datetime.fromtimestamp(message["time"]).strftime("%d/%m/%Y %H:%M:%S"))
                    self.add_to_chat(message["text"])
                    self.add_to_chat('')
                    last_time = message["time"]
            except:
                self.add_to_chat("ERROR: Receive message!")

            time.sleep(1)


app = QtWidgets.QApplication([])
window = MessengerApp()
window.show()
app.exec_()
