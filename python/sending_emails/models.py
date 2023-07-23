from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field

from .enums import EmailFormat


class EmailMessage(BaseModel):
    """Email message model"""
    recipients: List[str] = Field(description='List of emails to send email to.')
    subject: str = Field(description='Subject of the email.')
    content: str = Field(description='Content of the email.')
    attachments: Optional[List[Path] | None] = Field(description='List of files to send as attachments.')
    format: EmailFormat = Field(default=EmailFormat.TEXT, description='Format of the email contact. '
                                                                      'Either plain or html')
