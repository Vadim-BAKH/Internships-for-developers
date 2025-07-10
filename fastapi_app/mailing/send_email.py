"""Модуль отправки email-сообщений через SMTP."""

from email.message import EmailMessage

import aiosmtplib


async def send_email(
    recipient: str,
    subject: str,
    body: str,
):
    """
    Асинхронно отправляет email-сообщение получателю.

    :param recipient: Email-адрес получателя.
    :param subject: Тема письма.
    :param body: Текст письма.
    """
    admin_email = "admin@site.com"
    message = EmailMessage()
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        sender=admin_email,
        recipients=[recipient],
        hostname="maildev",
        port=1025,
    )
