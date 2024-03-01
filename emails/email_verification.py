from . import CLIENT_EMAIL, CLIENT_PASSWORD
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from . import VERIFICATION_EMAIL_TEMPLATE
from auth import EMAIL_KEY
import jwt
import datetime


def send_html_email(recipient_email, painter_info, base_url):
    message = MIMEMultipart("alternative")
    message["From"] = Header("Umurage art hub", "utf-8").encode()
    message["To"] = recipient_email
    message["Subject"] = "Email verification"
    painter_info["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    token = jwt.encode(
        painter_info,
        EMAIL_KEY,
    )

    token_link = f"{base_url}/verify?token={token}"

    plain_text = (
        VERIFICATION_EMAIL_TEMPLATE.format(token_link)
        .replace("<br>", "\n")
        .replace("<p>", "")
        .replace("</p>", "")
    )
    text_part = MIMEText(plain_text, "plain")
    message.attach(text_part)

    html_part = MIMEText(VERIFICATION_EMAIL_TEMPLATE.format(token_link), "html")
    message.attach(html_part)

    client = smtplib.SMTP("smtp.gmail.com", port=587)
    client.starttls()
    client.login(CLIENT_EMAIL, CLIENT_PASSWORD)
    client.send_message(message)
