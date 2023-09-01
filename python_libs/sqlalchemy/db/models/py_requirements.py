import logging
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy_utils import URLType

from python_libs.sqlalchemy.db.db_setup import Base
from python_libs.sqlalchemy.db.models.mixins import Timestamp

logger = logging.getLogger(__name__)


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


class PinnedRequirement(BaseModel):
    name: str
    version: str
    comment: Optional[str] = Field(default=None)


class PythonRequirement(Timestamp, Base):
    __tablename__ = "python_requirements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    latest_version = Column(String(15), unique=False, index=False, nullable=False)
    approved_version = Column(String(15), unique=False, index=False, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)
    home_page = Column(URLType, nullable=True)
    license = Column(String(128), unique=False, index=False, nullable=True)


class PythonRequirementPy(BaseModel):
    name: str
    latest_version: str
    approved_version: str
    group: Optional[str]
    environment: Optional[str]
    last_updated: Optional[datetime] = Field(default=datetime.now())
    home_page: Optional[HttpUrl]
    license: Optional[str]

    def to_req_line(self) -> str:
        if self.home_page is None:
            line = f'{self.name}=={self.approved_version}'
        else:
            line = f'{self.name}=={self.approved_version} # {self.home_page}'
        return line

    class Config:
        json_encoders = {
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }

    @property
    def latest_version_info(self):
        version_info = tuple(
            [
                int(num) if num.isdigit() else num
                for num in self.latest_version.replace("-", ".", 1).split(".")
            ]
        )
        return version_info

    @property
    def approved_version_info(self):
        version_info = tuple(
            [
                int(num) if num.isdigit() else num
                for num in self.approved_version.replace("-", ".", 1).split(".")
            ]
        )
        return version_info


class ParsedLine(BaseModel):
    line_number: int
    raw: str
    pinned: PinnedRequirement = Field(default=None)
    db_requirement: Optional[PythonRequirement] = Field(default=None)
