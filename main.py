from fastapi import FastAPI, Form, Depends, File, UploadFile
from Model import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Cors handle
app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Routes
# lallaalalal
@app.post('/api/')  # , response_model=User
async def add_row(db: Session = Depends(get_db), raw: RawBase = Depends(RawBase.as_form)):
    db_user = add_raw(db, raw)
    return db_user


# @app.get('/api/')  # , response_model=List[User]
# def get_user_view(db: Session = Depends(get_db)):
#     return get_users(db)

