from fastapi import FastAPI, Depends, File, UploadFile
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
@app.post('/user/')  # , response_model=User
async def create_user_view(user: User, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user


@app.get('/user/')  # , response_model=List[User]
def get_user_view(db: Session = Depends(get_db)):
    return get_users(db)


@app.post('/file/')
async def file_upload(file: UploadFile = File(...)):
    print(file)

@app.get("/")
async def root():
    return {"message": "Hello?"}
