import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import schemas, database, models
from fastapi import Depends, HTTPException,status, Response
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .config import settings 


# JWT config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRETE_KEY = settings.SECRET_KEY
ALGORITHM=  settings.ALGORITHM
TOKEN_EXPIRE_MINUTE=  settings.ACCESS_TOKEN_EXPIRE_MINUTES



def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTE)

    to_encode.update({"Exp": str(expire)})

    encoded_jwt =  jwt.encode(to_encode,SECRETE_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRETE_KEY,algorithms=[ALGORITHM])

        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
    
        token_data = schemas.TokenData(id=str(id))
    except (ExpiredSignatureError, InvalidTokenError):
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db) ):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.Users).filter(models.Users.user_id == token.id).first()

    return user


