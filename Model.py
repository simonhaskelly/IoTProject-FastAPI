import inspect
from pydantic import BaseModel, validator
from typing import Optional, List, Type, NewType
from DB import *
from datetime import datetime
from fastapi import Form
from sqlalchemy.dialects.postgresql import UUID
import uuid
from Password import get_password_hash

StringId = NewType('StringId', str)


def as_form(cls: Type[BaseModel]):
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls


class Raw(Base):
    __tablename__ = 'iot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    v = Column(Float, nullable=False)
    i = Column(Float, nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    time = Column(TIMESTAMP, index=True)

    # room = relationship("DBRoom", foreign_keys=[room_id])
    room = relationship("Room", back_populates="name")


class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(30), nullable=False)

    data = relationship("Raw", back_populates="id")

Base.metadata.create_all(bind=engine)


@as_form
class RawBase(BaseModel):
    v: float
    i: float
    room_id: int
    #time: Optional[str] = datetime.now()

    class Config:
        orm_mode = True


class RoomBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


def add_raw(db: Session, raw: RawBase):
    db_raw = Raw(**raw.dict())
    db.add(db_raw)
    db.commit()
    db.refresh(db_raw)
    return db_raw
# def get_users(db: Session):
#     return db.query(DBUser).all()
#
#
# def create_user(db: Session, user: User):
#     hashed_password = get_password_hash(user.password1)
#     db_user = DBUser(username=user.username, password=hashed_password, lineID=user.lineID,
#                      isAdmin=user.isAdmin, isVolunteer=user.isVolunteer, isPublicHealth=user.isPublicHealth,
#                      create=datetime.now())
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

