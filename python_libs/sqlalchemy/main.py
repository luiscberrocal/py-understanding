from python_libs.sqlalchemy.db.db_setup import engine
from python_libs.sqlalchemy.db.models import py_requirements

py_requirements.Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    pass
