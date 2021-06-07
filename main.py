from fastapi import FastAPI, Depends
from Model import *

app = FastAPI()


@app.post('/places/', response_model=Place)
async def create_places_view(place: Place, db: Session = Depends(get_db)):
    db_place = create_place(db, place)
    return db_place


@app.get('/places/', response_model=List[Place])
def get_places_view(db: Session = Depends(get_db)):
    return get_places(db)


@app.get('/place/{place_id}')
def get_place_view(place_id: int, db: Session = Depends(get_db)):
    return get_place(db, place_id)


@app.get("/")
async def root():
    return {"message": "Hello World"}