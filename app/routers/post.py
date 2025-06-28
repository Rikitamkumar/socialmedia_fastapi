from fastapi import FastAPI, Response,HTTPException,status, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from app import models,schemas, OAuth2
from app.database import get_db



router = APIRouter(prefix="/posts", tags= ['Posts'])


@router.get("/", response_model=List[schemas.PostOut])
async def root(db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user), limit:int=8, skip: int =0, search: Optional[str] = ""):

    fetch_post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # cursor.execute(""" SELECT * FROM posts; """) # using regular  raw SQL method
    # all_post = cursor.fetchall()
    
    return fetch_post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):
    
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *  """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # Above commented statment used the regular raw SQL method


    new_post  = models.Post(user_id= current_user.user_id,**post.dict()) #This is the standard and preferable method, as we first convert the model (table) into a dictionary and then unpack it using operator **

    # new_post  = models.Post(title = post.title, content = post.content, published = post.published)  # This is a manual way to extract the table column, but it's not preferable. 

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):
    
    
    # cursor.execute(""" SELECT * FROM posts WHERE id =%s""", (str(id)))
    # result = cursor.fetchone()
    
    # Above commented statment used the regular raw SQL method

    fetch_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not fetch_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no post with ID {id}")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"There is no post with ID {id}"}


    return fetch_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):

    # cursor.execute(""" DELETE FROM posts where id = %s RETURNING *""",(str(id)),)
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    # Above commented statment used the regular raw SQL method


    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    print(current_user.user_id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"There is no post with ID {id}")
    
    if current_user.user_id != post.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"You are not authorized to delete this post.")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id:int, post1: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s where id =%s RETURNING *""",(post.title,post.content, post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    # Above commented statment used the regular raw SQL method

    post_query = db.query(models.Post).filter(models.Post.id == id)
    

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"There is no post with ID {id}")
    
    if current_user.user_id != post.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"You are not authorized to update this post.")
    
    post_query.update(post1.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()