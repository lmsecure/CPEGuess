from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

abs_path = os.path.abspath(__file__)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.dirname(__file__)}/db.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,pool_size=0, max_overflow=0,connect_args={"check_same_thread": False,}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
