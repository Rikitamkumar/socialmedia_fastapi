from fastapi import FastAPI
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
import time
from sqlalchemy.orm import Session 
from psycopg2.extras import RealDictCursor
from app import models, schemas,utils
from .database import engine, get_db

from .routers import post, user 


models.Base.metadata.create_all(bind=engine)  # It tells SQLAlchemy: Create all the tables in the database that are defined in the models — if they don’t already exist.

app = FastAPI()


while True: # Use to 
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


app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
async def root():
    
    return {"message": "This is a root page"}

