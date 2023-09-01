import logging
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy_utils import URLType

from python_libs.sqlalchemy.db.db_setup import Base
from python_libs.sqlalchemy.db.models.mixins import Timestamp

logger = logging.getLogger(__name__)


class PythonRequirement(Timestamp, Base):
    __tablename__ = "python_requirements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    latest_version = Column(String(15), unique=False, index=False, nullable=False)
    approved_version = Column(String(15), unique=False, index=False, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)
    home_page = Column(URLType, nullable=True)
    license = Column(String(128), unique=False, index=False, nullable=True)
