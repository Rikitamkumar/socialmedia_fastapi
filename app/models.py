from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base

class Post(Base):

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable= False)
    
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer,ForeignKey('users.user_id',ondelete='CASCADE'),nullable=False)

    owner = relationship("Users")

class Users(Base):

    __tablename__ = "users"
    user_id = Column(Integer, primary_key= True, nullable=False) 
    email = Column(String, nullable = False, unique= True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Like(Base):
    __tablename__ ='likes'

    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key= True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)







    
# With SQLAlchemy, updating the structure of an existing table (like adding or modifying columns) doesn’t work directly through the model.

# SQLAlchemy models can reflect and interact with existing tables. But if we change a model’s structure (e.g., add a new column), SQLAlchemy won’t automatically alter the actual database schema.

# For structural changes, you use tools like Alembic, which is designed for migrations in SQLAlchemy projects.