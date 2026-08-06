import os
import smtplib
from email.message import EmailMessage


def send_report(report: str) -> None:
    """Send the weather report by email."""

    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_recipient = os.getenv("EMAIL_RECIPIENT")

    if not email_address:
        raise ValueError("EMAIL_ADDRESS is not configured.")

    if not email_password:
        raise ValueError("EMAIL_PASSWORD is not configured.")

    if not email_recipient:
        raise ValueError("EMAIL_RECIPIENT is not configured.")

    message = EmailMessage()
    message["Subject"] = "Daily Weather Report"
    message["From"] = email_address
    message["To"] = email_recipient
    message.set_content(report)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_address, email_password)
            server.send_message(message)
    except smtplib.SMTPException as error:
        raise RuntimeError("Failed to send the email report.") from error