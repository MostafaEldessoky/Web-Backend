import shutil
from fastapi import APIRouter , Depends  , HTTPException , status , UploadFile 
from sqlmodel import  Session , select , desc
from data.db_connection import get_db , posts , users , redis_db
from .user import get_payload
from typing import List


router = APIRouter()


@router.get("/get_posts/")
async def get_posts(offset : int ,limit : int , session : Session = Depends(get_db)) -> List[dict]:
    query = session.exec(select(posts).order_by(desc(posts.post_time)).offset(offset).limit(limit)).all()
    query = [{"post": i,"comments" :  i.post_comments} for i in query]
    return query


@router.post("/upload_image")
async def upload_image(image : UploadFile ,user : users = Depends(get_payload)):
    image_counter = redis_db.get(name = "image_counter")  
    image_url = image.filename.split(".")
    image_url = "/images/"+f"image_{image_counter}"+"."+image_url[1]
    redis_db.incr("image_counter")
    with open(file="."+image_url,mode="w+b") as file:
        shutil.copyfileobj(image.file , file)
    return {"username" : user.username , "url" : "http://127.0.0.1:8000"+image_url}

              

@router.post("/make_post")
async def make_post(post : posts ,user : users = Depends(get_payload), session : Session = Depends(get_db)) -> posts:
    post.username = user.username
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.delete("/delete_post/{id}")
async def delete_post(id : int ,user : users = Depends(get_payload), session : Session = Depends(get_db)):
    try:
        query = session.exec(select(posts).where(posts.id == id)).one()
        if query != None:
            if query.username == user.username:
                session.delete(query)
                session.commit()
                return query
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    

