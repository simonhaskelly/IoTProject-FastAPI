from pydantic import BaseModel
from typing import Optional, List
from DB import *


class DBPlace(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String, nullable=True)
    coffee = Column(Boolean)
    wifi = Column(Boolean)


Base.metadata.create_all(bind=engine)


class Place(BaseModel):
    name: str
    description: Optional[str] = None
    coffee: bool
    wifi: bool

    class Config:
        orm_mode = True


def get_place(db: Session, place_id: int):
    return db.query(DBPlace).where(DBPlace.id == place_id).first()


def get_places(db: Session):
    return db.query(DBPlace).all()


def create_place(db: Session, place: Place):
    db_place = DBPlace(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place