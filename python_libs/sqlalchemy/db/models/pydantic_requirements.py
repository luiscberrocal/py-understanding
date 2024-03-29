import logging
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

logger = logging.getLogger(__name__)


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


class PinnedRequirement(BaseModel):
    name: str
    version: str
    comment: Optional[str] = Field(default=None)


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
