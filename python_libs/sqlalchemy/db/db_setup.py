from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://gwen@localhost/fast_lms"
SQLITE_FILE = Path(__file__).parent / 'requirements_db.sqlite'
SQLALCHEMY_DATABASE_URL = f"sqlite:///{SQLITE_FILE}"

# future = True allows to use async calls to sqlalchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={}, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()


# DB Utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == '__main__':
    print(f'{SQLITE_FILE=}')
    print(SQLITE_FILE.exists())
    print(f'{SQLALCHEMY_DATABASE_URL=}')
