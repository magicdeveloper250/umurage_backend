import smtplib
from email.header import Header
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_html_email(recipient_email, subject, html_content):
    """Sends an HTML email asynchronously using aiosmtplib."""

    message = MIMEMultipart("alternative")
    message["From"] = Header(
        "Umurage art hub", "utf-8"
    ).encode()  # Correct usage of Header
    message["To"] = recipient_email
    message["Subject"] = subject

    # Attach plain text alternative for email clients that don't support HTML
    plain_text = (
        html_content.replace("<br>", "\n").replace("<p>", "").replace("</p>", "")
    )
    text_part = MIMEText(plain_text, "plain")
    message.attach(text_part)

    # Attach HTML content
    html_part = MIMEText(html_content, "html")
    message.attach(html_part)

    client = smtplib.SMTP("smtp.gmail.com", port=587)
    client.starttls()
    client.login("impanomanzienock@gmail.com", "qsygyjmcuneelfvx")
    client.send_message(message)
