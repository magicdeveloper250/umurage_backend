from email.mime.multipart import MIMEMultipart
from . import CLIENT_EMAIL, CLIENT_PASSWORD
from typing import Any, Iterable, Mapping
from . import CUSTOMER_EMAIL_TEMPLATE
from email.mime.text import MIMEText
from collections.abc import Callable
from email.header import Header
from threading import Thread
import smtplib


class CustomerEmailWorker(Thread):
    def __init__(
        self,
        group: None = None,
        target=None,
        name=None,
        args: Iterable[Any] = ...,
        kwargs=None,
        *,
        daemon=None
    ) -> None:
        super(CustomerEmailWorker, self).__init__(
            group, target, name, args, kwargs, daemon=daemon
        )
        self.daemon = True
        self.data = kwargs

    def send_html_email(self):
        message = MIMEMultipart("alternative")
        message["From"] = Header("Umurage art hub", "utf-8").encode()
        message["To"] = self.data.get("email")
        message["Subject"] = "Exhibition registration info"
        plain_text = (
            CUSTOMER_EMAIL_TEMPLATE.format(*self.data.get("message"))
            .replace("<br>", "\n")
            .replace("<p>", "")
            .replace("</p>", "")
        )
        text_part = MIMEText(plain_text, "plain")
        message.attach(text_part)

        html_part = MIMEText(
            CUSTOMER_EMAIL_TEMPLATE.format(*self.data.get("message")), "html"
        )
        message.attach(html_part)
        client = smtplib.SMTP("smtp.gmail.com", port=587)
        client.starttls()
        client.login(CLIENT_EMAIL, CLIENT_PASSWORD)
        client.send_message(message)

    def run(self):
        self.send_html_email()
