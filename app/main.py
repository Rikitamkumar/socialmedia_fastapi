from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
import time
from sqlalchemy.orm import Session 
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):  # This model(or schema) will be used when using regular raw SQL method
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='socialmedia_fastapi', user= 'postgres', password ='rikitam123', cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successdull")
        break
    except Exception as e:
        print("Connection Failed due to: ",e)
        time.sleep(2)

# def find_post(id):
#     for p in my_post:
#         if p['id']==id:
#             return p

def find_post_index(id):

    for index,post in enumerate(my_post):
        if post['id'] == id:
            return index


@app.get("/")
async def root():
    
    return {"message": "This is a root page"}

@app.get("/posts")
async def root(db: Session = Depends(get_db)):

    fetch_post = db.query(models.Post).all()

    # cursor.execute(""" SELECT * FROM posts; """) # using regular  raw SQL method
    # all_post = cursor.fetchall()
    
    return {"date": fetch_post}

#belwo route is just for testing purpose - ignore it
@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    
    return{"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *  """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # Above commented statment used the regular raw SQL method


    new_post  = models.Post(**post.dict()) #This is the standard and preferable method, as we first convert the model (table) into a dictionary and then unpack it using operator **

    # new_post  = models.Post(title = post.title, content = post.content, published = post.published)  # This is a manual way to extract the table column, but it's not preferable. 
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}

@app.get("/posts/{id}")
def get_post(id: int): # if use manual methid pass the reference of Response to the fucntion
    
    #result = find_post(id)
    cursor.execute(""" SELECT * FROM posts WHERE id =%s""", (str(id)))
    result = cursor.fetchone()
    # result = next((p for p in my_post if p["id"]==int(id) ),None) # This is a generator expression (next() function is used to get the next item from an iterator - like a generator or an iterable)
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no post with ID {id}")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"There is no post with ID {id}"}


    return {"post detail":result}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute(""" DELETE FROM posts where id = %s RETURNING *""",(str(id)),)
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"There is no post with ID {id}")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post: Post):

    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s where id =%s RETURNING *""",(post.title,post.content, post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"There is no post with ID {id}")
    
    return {"Updated Post": updated_post}