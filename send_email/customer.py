from . import CLIENT_EMAIL, CLIENT_PASSWORD
from email.header import Header
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_html_email(recipient_email, subject, html_content):

    message = MIMEMultipart("alternative")
    message["From"] = Header("Umurage art hub", "utf-8").encode()
    message["To"] = recipient_email
    message["Subject"] = subject

    plain_text = (
        html_content.replace("<br>", "\n").replace("<p>", "").replace("</p>", "")
    )
    text_part = MIMEText(plain_text, "plain")
    message.attach(text_part)

    html_part = MIMEText(html_content, "html")
    message.attach(html_part)

    client = smtplib.SMTP("smtp.gmail.com", port=587)
    client.starttls()
    client.login(CLIENT_EMAIL, CLIENT_PASSWORD)
    client.send_message(message)
