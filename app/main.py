from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor
app = FastAPI()


my_post = [{"title": "title of post 1", "content": "content of post 1", "id":1}, {"title": "My favourit game", "content": "I love to play GTA 5", "id": 2}]

class Post(BaseModel):
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

# class UpdatePost(BaseModel):
#     title: Optional[str] = None
#     content: Optional[str] = None
#     rating: Optional[int] = None

def find_post(id):
    for p in my_post:
        if p['id']==id:
            return p

def find_post_index(id):

    for index,post in enumerate(my_post):
        if post['id'] == id:
            return index


@app.get("/")
async def root():

    cursor.execute(""" SELECT * FROM posts; """)
    all_post = cursor.fetchall()
    return {"date": all_post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *  """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
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