from fastapi import FastAPI, APIRouter, status,HTTPException, Depends, Response
from sqlalchemy.orm import Session
from app.database import get_db 
from app import schemas,models,utils, OAuth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def  user_login(user_credential : OAuth2PasswordRequestForm = Depends(), db: Session =Depends(get_db)):

    user =  db.query(models.Users).filter(models.Users.email == user_credential.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f" Invalid Credentials")
    
    if not utils.verify_password(user_credential.password, user.password):

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials ")
    
    access_token = OAuth2.create_access_token(data = {"user_id": user.user_id})
    
    return {"access_token": access_token, "token_type": "bearer" }



"""
If frontend sends JSON (e.g., React, Axios, fetch) ---> Use : UserLogin schema (Pydantic)

If frontend sends Form (e.g., Swagger UI, Postman) ----> Use : OAuth2PasswordRequestForm

"""

