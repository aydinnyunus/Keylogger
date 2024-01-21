# Program objectives
This is a keylogger, use it for testing purposes.
You will gather keyboard strokes, mouse movements, screenshots and microphone input.
All the collected info will be sent via email every defined time interval.

## Program phases

### Imports

- **logging**: Used for logging messages.
- **os**: Provides a way of using operating system-dependent functionality.
- **platform**: Provides an interface to various services that interact with the operating system.
- **smtplib**: Provides an SMTP client session to send emails.
- **socket**: Provides access to the underlying operating system's socket services.
- **threading**: Provides threading support.
- **wave**: Used for reading and writing WAV files.
- **pyscreenshot**: Captures screenshots.
- **sounddevice**: Provides an interface to play and record audio.
- **pynput**: Library for monitoring input devices.

Note: you should run
```python
pip install -r requirements.txt
```

### Configuration

Defines email address and password for sending logs.
For this project, I created an email account using [mailtrap](https://mailtrap.io).
Specifies the interval for sending reports (SEND_REPORT_EVERY).

### KeyLogger Class

- Monitors keyboard events using pynput library.
- Records mouse movements, clicks, and scrolls.
- Saves the logged data to a string (self.log).
- Sends email reports with logged data.
- Collects system information (hostname, IP address, processor, system, machine).
- Captures microphone input and sends it via email.
- Takes screenshots and sends them via email.
- The run method starts the keylogger by setting up keyboard and mouse listeners.
- Performs some cleanup actions based on the operating system if the target computer finds the code and open the file. In this way, the target cannot see your email and password.

### Execution

Creates an instance of the KeyLogger class with the specified email, password, and reporting interval.
Calls the run method to start the keylogger.
