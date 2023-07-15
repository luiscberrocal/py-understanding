import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from python.sending_emails.enums import EmailFormat
from python.sending_emails.models import EmailMessage


class MailServer:

    def __init__(self, sender_email: str, password: str):
        self.sender_email = sender_email
        self.password = password

    def send_email(self, email_message: EmailMessage):
        # The mail addresses and password
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = ', '.join(email_message.recipients)
        message['Subject'] = email_message.subject
        # The subject line
        # The body and the attachments for the mail
        if email_message.format == EmailFormat.HTML:
            message.add_header('Content-Type', 'text/html')
        message.attach(MIMEText(email_message.content, email_message.format.value))
        if email_message.attachments is not None:
            for attachment in email_message.attachments:
                attach_file = open(attachment, 'rb')  # Open the file as binary mode
                payload = MIMEBase('application', 'octate-stream')
                payload.set_payload(attach_file.read())
                encoders.encode_base64(payload)  # encode the attachment
                # add payload header with filename
                fn = os.path.basename(attachment)
                payload.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {fn}",
                )
                message.attach(payload)
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(self.sender_email, self.password)  # login with mail_id and password
        text = message.as_string()
        senders_response = session.sendmail(self.sender_email, email_message.recipients, text)
        session.quit()
        return senders_response

if __name__ == '__main__':
    from dotenv import load_dotenv
    from pathlib import Path
    environment_folder = Path(__file__).parent.parent.parent / '.envs'
    environment_file = environment_folder / 'sending_emails' / 'gmail_secrets.txt'
    dotenv_path = Path(environment_file)
    load_dotenv(dotenv_path=dotenv_path)
    email = 'luis.berrocal.1942@gmail.com'
    
    # print(os.getenv('GMAIL_USER'))
