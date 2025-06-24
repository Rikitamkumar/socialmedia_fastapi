from fastapi import FastAPI, responses, status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app import schemas,models, utils
from app.database import get_db

router = APIRouter(prefix="/users")


@router.post("/",status_code=status.HTTP_201_CREATED ,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    fetch_user = db.query(models.Users).filter(models.Users.user_id == id).first()

    if not fetch_user:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No user exits with id {id} ")

    return fetch_user
