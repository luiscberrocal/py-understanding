from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SpeedSample(BaseModel):
    machine: str
    download: float
    upload: float
    elapsed_time: float
    date: datetime
    ssid: Optional[str]
