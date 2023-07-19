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
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = ', '.join(email_message.recipients)
        message['Subject'] = email_message.subject

        # Set content type based on email format
        if email_message.format == EmailFormat.HTML:
            message.attach(MIMEText(email_message.content, 'html'))
        else:
            message.attach(MIMEText(email_message.content, 'plain'))

        # Attach files if available
        if email_message.attachments:
            for attachment in email_message.attachments:
                with open(attachment, 'rb') as attach_file:
                    payload = MIMEBase('application', 'octate-stream')
                    payload.set_payload(attach_file.read())
                    encoders.encode_base64(payload)  # encode the attachment
                    payload.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment)}")
                    message.attach(payload)

        # Create SMTP session for sending the mail
        with smtplib.SMTP('smtp.gmail.com', 587) as session:
            session.starttls()  # enable security
            session.login(self.sender_email, self.password)  # login with mail_id and password
            text = message.as_string()
            senders_response = session.sendmail(self.sender_email, email_message.recipients, text)

        return senders_response
