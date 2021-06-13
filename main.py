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
    ret = add_raw(db, raw)
    return ret


@app.get('/api/')  # , response_model=List[User]
async def get_user_view(db: Session = Depends(get_db)):
    ret = get_data_today(db)
    return ret

