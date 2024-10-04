
from sqlmodel import SQLModel , create_engine , Session , Relationship , Field
from typing import List
from passlib.context import CryptContext
from datetime import datetime
from env import psgr_db , rds_host , rds_port
from redis_om import get_redis_connection 

redis_db = get_redis_connection(host=rds_host,port=rds_port)

postgres_db = create_engine(psgr_db)

def map_tables():
    SQLModel.metadata.create_all(postgres_db)

def get_db():
    with Session(postgres_db) as session:
        yield session


hashed = CryptContext(schemes=["bcrypt"], deprecated="auto")

def make_hash(password : str) -> str:
    return hashed.hash(password)

def verfiy_password(hash_password,password) -> bool:
    return hashed.verify(password,hash_password)


class users(SQLModel, table = True):
    username : str = Field(...,primary_key=True,unique=True,index=True)
    password : str 
    is_active : bool 

    user_posts : List["posts"] =  Relationship(back_populates="post_owner",cascade_delete=True)
    user_comments : List["comments"] = Relationship(back_populates="comment_owner")

    def __init__(self,username,password):
        self.username = username
        self.password = make_hash(password)
        self.is_active  = True

class posts(SQLModel, table =True):
    id : int = Field(primary_key=True,index=True)
    username : str = Field(...,foreign_key="users.username",index=True)
    image_url : str 
    caption : str
    post_time : datetime

    post_comments : List["comments"] = Relationship(back_populates="comment_on_post",cascade_delete=True)
    post_owner : users = Relationship(back_populates="user_posts")

    def __init__(self,image_url,caption, username = ""):
        self.username = username
        self.image_url =image_url
        self.caption  = caption
        self.post_time = datetime.now()


class comments(SQLModel, table = True):
    id : int = Field(primary_key=True)
    post_id : int = Field(foreign_key="posts.id")
    username :str = Field(foreign_key="users.username")
    comment : str
    comment_time : datetime 

    comment_on_post : "posts" = Relationship(back_populates="post_comments")
    comment_owner : users = Relationship(back_populates="user_comments")

    def __init__(self,post_id,comment, username = ""):
        self.post_id = post_id
        self.username = username
        self.comment = comment
        self.comment_time  = datetime.now()







