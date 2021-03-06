import inspect
from pydantic import BaseModel, validator
from typing import Optional, List, Type, NewType
from DB import *
from datetime import datetime,date
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
    v1 = Column(Float, nullable=False)
    i1 = Column(Float, nullable=False)
    v2 = Column(Float, nullable=False)
    i2 = Column(Float, nullable=False)
    v3 = Column(Float, nullable=False)
    i3 = Column(Float, nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    time = Column(TIMESTAMP, index=True)

    # room = relationship("DBRoom", foreign_keys=[room_id])
    room = relationship("Room", back_populates="data")  # Sqlalchemy magic /*


class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(30), nullable=False)

    data = relationship("Raw", back_populates="room")  # Sqlalchemy magic /*

Base.metadata.create_all(bind=engine)


@as_form
class RawBase(BaseModel):
    v1: float
    i1: float
    v2: float
    i2: float
    v3: float
    i3: float
    # room_id: int
    #time: Optional[str] = datetime.now()

    class Config:
        orm_mode = True


class RoomBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class When(BaseModel):
    when: datetime


def add_raw(db: Session, raw: RawBase):
    db_raw = Raw(v1=raw.v1, i1=raw.i1, v2=raw.v2, i2=raw.i2, v3=raw.v3, i3=raw.i3,
                 room_id=1, time=datetime.now())
    db.add(db_raw)
    db.commit()
    db.refresh(db_raw)
    return db_raw


def get_last(db: Session):
    return db.query(Raw).order_by(-Raw.id).first()


def get_chart_test(db: Session):
    return db.query(Raw).all()


def get_data_today(db: Session):
    return db.query(Raw).filter(func.DATE(Raw.time) == date.today()).all()


def get_data_when(db: Session, when: When):
    return db.query(Raw).filter(func.DATE(Raw.time) == when).all()
