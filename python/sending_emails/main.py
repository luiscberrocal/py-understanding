import os

from python.sending_emails.enums import EmailFormat
from python.sending_emails.gmail import MailServer
from python.sending_emails.models import EmailMessage


def get_secrets():
    from dotenv import load_dotenv
    from pathlib import Path
    environment_folder = Path(__file__).parent.parent.parent / '.envs'
    environment_file = environment_folder / 'sending_emails' / 'gmail_secrets.txt'
    dotenv_path = Path(environment_file)
    load_dotenv(dotenv_path=dotenv_path)
    email = os.getenv('GMAIL_USER')
    password = os.getenv('GMAIL_SECRET')
    return email, password


def send_text_email_no_attachments():
    email, password = get_secrets()

    mail_server = MailServer(sender_email=email, password=password)
    content = """Good morning:
    This email is to report that I started working at 7:30 am.
    """
    email = EmailMessage(recipients=[email], subject='Daily Start of Labor Report',
                         content=content, format=EmailFormat.TEXT)
    response = mail_server.send_email(email)


def send_text_email_invalid_credentials():
    email, password = get_secrets()
    password = 'invalid'

    mail_server = MailServer(sender_email=email, password=password)
    content = """Good morning:
    This email is to report that I started working at 7:30 am.
    """
    email = EmailMessage(recipients=[email], subject='Daily Start of Labor Report',
                         content=content, format=EmailFormat.TEXT)
    response = mail_server.send_email(email)
    print(response)


def send_html_email_no_attachments():
    email, password = get_secrets()

    mail_server = MailServer(sender_email=email, password=password)
    content = """Good morning:
    This email is to report that I started working at <span style="color:blue;background:pink;font-size:16px;font-weight:bold;">7:30 am</span>.
    """
    email = EmailMessage(recipients=[email], subject='Daily Start of Labor Report',
                         content=content, format=EmailFormat.HTML)
    response = mail_server.send_email(email)


if __name__ == '__main__':
    send_html_email_no_attachments()
