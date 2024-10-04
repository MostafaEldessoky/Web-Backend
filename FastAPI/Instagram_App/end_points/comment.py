from fastapi import APIRouter
from fastapi import APIRouter , Depends  , HTTPException , status
from sqlmodel import  Session , select
from data.db_connection import get_db , users , comments
from .user import get_payload



router = APIRouter()


@router.post("/make_comment")
async def make_comment(comment : comments , user : users = Depends(get_payload), session : Session = Depends(get_db)):
    comment.username = user.username
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


@router.delete("/delete_comment/{id}")
async def delete_comment(id : int,user : users = Depends(get_payload), session : Session = Depends(get_db)):
    try :
        query = session.exec(select(comments).where(comments.id == id)).one()
        if query != None:
            if query.username == user.username:
                session.delete(query)
                session.commit()
                return query
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)