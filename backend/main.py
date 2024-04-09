from fastapi import FastAPI
import models
from db import engine, LocalSession
import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = LocalSession()
    
    try:
        yield db
    finally:
        db.close()
        