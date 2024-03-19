from email.mime.multipart import MIMEMultipart
from . import CLIENT_EMAIL, CLIENT_PASSWORD
from typing import Any, Iterable, Mapping
from . import VERIFICATION_EMAIL_TEMPLATE
from email.mime.text import MIMEText
from collections.abc import Callable
from email.header import Header
from threading import Thread
from auth import EMAIL_KEY
import datetime
import smtplib
import jwt
import os


class EmailVerificationWorker(Thread):
    def __init__(
        self,
        group: None = None,
        target: Callable[..., object] | None = None,
        name: str | None = None,
        args: Iterable[Any] = ...,
        kwargs: Mapping[str, Any] | None = None,
        *,
        daemon: bool | None = None,
    ) -> None:
        super(EmailVerificationWorker, self).__init__(
            group, target, name, args, kwargs, daemon=daemon
        )
        # self.daemon = True
        self.data = kwargs

    def send_html_email(self):
        message = MIMEMultipart("alternative")
        message["From"] = Header("Umurage art hub", "utf-8").encode()
        message["To"] = self.data.get("email")
        message["Subject"] = "Email verification"
        self.data.get("painter_info")[
            "exp"
        ] = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        data = {
            "id": self.data.get("painter_info").get("id"),
            "email": self.data.get("painter_info").get("email"),
        }

        token = jwt.encode(
            data,
            EMAIL_KEY,
        )
        token_link = f"{os.environ.get('FRONT_END_SERVER')}/verify-email?token={token}"
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

    def run(self):
        self.send_html_email()
