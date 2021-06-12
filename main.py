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
# just in case that we cant build JSON (Arduino shit) - multi-part data is accepted here
@app.post('/api/')  # , response_model=User
async def add_raw(db: Session = Depends(get_db), raw: RawBase = Depends(RawBase.as_form)):
    db_user = add_raw(db, raw)
    return db_user


@app.get('/api/')
async def get_data(db: Session = Depends(get_db), when: PlotDataIn = Depends(PlotDataIn)):
    if when.when is not None:
        return get_data_today(db)