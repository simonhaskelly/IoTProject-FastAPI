from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Boolean, Column, Float, String, Integer, Text, TIMESTAMP

# SqlAlchemy init
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:h2me053556389DE@localhost:5432/mfucare'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SqlAlchemy dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()