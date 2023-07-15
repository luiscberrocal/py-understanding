from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field

from .enums import EmailFormat


class EmailMessage(BaseModel):
    recipients: List[str]
    subject: str
    content: str
    attachments: Optional[List[Path] | None]
    format: EmailFormat = Field(default=EmailFormat.TEXT)
