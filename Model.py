from pydantic import BaseModel, validator
from typing import Optional, List
from DB import *
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from Password import get_password_hash


def get_now():
    return datetime.now()


class DBUser(Base):
    __tablename__ = 'users'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(30))
    password = Column(Text)
    lineID = Column(String(30))
    isAdmin = Column(Boolean)
    isVolunteer = Column(Boolean)
    isPublicHealth = Column(Boolean)
    create = Column(TIMESTAMP)


Base.metadata.create_all(bind=engine)


class User(BaseModel):
    username: str
    password1: str
    password2: str
    lineID: str
    isAdmin: bool
    isVolunteer: bool
    isPublicHealth: bool

    @validator('username')
    def username_max(cls, v):
        if len(str(v)) > 30:
            raise ValueError('username must lower than 30 chars')
        return v

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v

    class Config:
        orm_mode = True


def get_users(db: Session):
    return db.query(DBUser).all()


def create_user(db: Session, user: User):
    hashed_password = get_password_hash(user.password1)
    db_user = DBUser(username=user.username, password=hashed_password, lineID=user.lineID,
                     isAdmin=user.isAdmin, isVolunteer=user.isVolunteer, isPublicHealth=user.isPublicHealth,
                     create=datetime.now())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

