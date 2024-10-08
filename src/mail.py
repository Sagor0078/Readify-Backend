from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

MAIL_USERNAME = "musagor78@gmail.com"
MAIL_PASSWORD = "sqkn zmbu sjnr nrzk"
MAIL_SERVER="smtp.gmail.com"
MAIL_PORT=587
MAIL_FROM="musagor78@gmail.com"
MAIL_FROM_NAME="Book-Store"
DOMAIN="localhost:8000"



mail_config = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(BASE_DIR, "templates"),
)

mail = FastMail(config=mail_config)


def create_message(recipients: list[str], subject: str, body: str, template_name: str = None):
    """
    Creates a message schema for sending an email.

    Args:
        recipients (list[str]): The list of email recipients.
        subject (str): The email subject.
        body (str): The email body.
        template_name (str, optional): The name of the email template to use. Defaults to None.

    Returns:
        MessageSchema: The created message schema.
    """

    if template_name:
        template_path = Path(BASE_DIR, "templates", template_name)
        with open(template_path, "r") as f:
            template_content = f.read()
        body = template_content.format(**body)  # Replace placeholders in the template

    message = MessageSchema(
        recipients=recipients, subject=subject, body=body, subtype=MessageType.html
    )
    return message


async def send_email(recipients: list[str], subject: str, body: str, template_name: str = None):
    """
    Sends an email using the specified recipients, subject, body, and template.

    Args:
        recipients (list[str]): The list of email recipients.
        subject (str): The email subject.
        body (str): The email body.
        template_name (str, optional): The name of the email template to use. Defaults to None.

    Raises:
        Exception: If an error occurs during email sending.
    """

    message = create_message(recipients, subject, body, template_name)
    try:
        await mail.send_message(message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")