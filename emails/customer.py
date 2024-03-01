from . import CLIENT_EMAIL, CLIENT_PASSWORD
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from . import CUSTOMER_EMAIL_TEMPLATE


def send_html_email(recipient_email, html_content):

    message = MIMEMultipart("alternative")
    message["From"] = Header("Umurage art hub", "utf-8").encode()
    message["To"] = recipient_email
    message["Subject"] = "Exhibition registration info"

    plain_text = (
        CUSTOMER_EMAIL_TEMPLATE.format(*html_content)
        .replace("<br>", "\n")
        .replace("<p>", "")
        .replace("</p>", "")
    )
    text_part = MIMEText(plain_text, "plain")
    message.attach(text_part)

    html_part = MIMEText(CUSTOMER_EMAIL_TEMPLATE.format(*html_content), "html")
    message.attach(html_part)

    client = smtplib.SMTP("smtp.gmail.com", port=587)
    client.starttls()
    client.login(CLIENT_EMAIL, CLIENT_PASSWORD)
    client.send_message(message)
