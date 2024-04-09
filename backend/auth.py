from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from db import LocalSession
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'g31cS4yK0PzRt98iE5V6m7pQrS1tUvWx'
HASH_ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class Token(BaseModel):
    access_token: str
    token_type: str

class CreateUserRequest(BaseModel):
    username: str
    password: str
    
    
class VerifyTokenRequest(BaseModel):
    token: str
    
def get_db():
    db = LocalSession()
    
    try: 
        yield db
    finally: 
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    logging.info('Checking if user already exists in database...')
    existing_user = db.query(Users).filter(Users.username == create_user_request.username).first()
    
    if existing_user:
        logger.warn('User already exists')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    
    create_user_model = Users(
        username=create_user_request.username,
        password_hash=bcrypt_context.hash(create_user_request.password)
    )
    
    logging.info('Adding user to database...')
    db.add(create_user_model)
    db.commit()
    
@router.post("/token", response_model=Token, status_code=status.HTTP_201_CREATED)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    logger.info('Authenticating user...')
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        logger.warning("Could not authenticate user")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.') 
    
    logger.info('Creating access token...')
    token = create_access_token(user.username, user.id, timedelta(seconds=10))
    
    return {'access_token': token, 'token_type': 'bearer'}


@router.post("/verifytoken", status_code=status.HTTP_200_OK)
async def verify_token(verify_token_request: VerifyTokenRequest): 
    try:
        logger.info('Verifying user token...')
        options = {"verify_exp": True}
        payload = jwt.decode(verify_token_request.token, SECRET_KEY, algorithms=[HASH_ALGORITHM], options=options)
        username: str = payload.get("sub")
        
        return {"username": username, "valid": True}
    except JWTError:
        logger.warning('Invalid token')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    
    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.password_hash):
        return False
    
    return user

def create_access_token(username: str, user_id: int, expire_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expire_delta
    encode.update({'exp': expires})
    
    return jwt.encode(encode, SECRET_KEY, algorithm=HASH_ALGORITHM)
