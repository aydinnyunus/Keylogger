import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_mail_with_attachment(
    smtp_server,
    smtp_port,
    email_address,
    email_password,
    email_sender,
    email_receiver,
    cc="",
    path_to_attachment="",
    attachments=[],
    subject="",
    body="",
):
    message = MIMEMultipart()
    message["From"] = email_sender
    message["To"] = email_receiver
    message["Cc"] = cc
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    for attachment in attachments:  # [filename_1, filename_2]
        # Open the file as binary mode
        attach_file = open("{0}/{1}".format(path_to_attachment, attachment), "rb")
        payload = MIMEBase("application", "octate-stream")
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)  # encode the attachment

        # Add payload header with filename
        payload.add_header("Content-Disposition", f"attachment; filename={attachment}")
        message.attach(payload)

    session = smtplib.SMTP(smtp_server, smtp_port)
    # session.starttls()  # Enable security
    session.login(email_address, email_password)
    text = message.as_string()
    session.sendmail(email_sender, email_receiver, text)
    session.quit()

    return True
