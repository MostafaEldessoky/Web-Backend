from sqlmodel import  Session , select
from fastapi import Depends , APIRouter , HTTPException , status
from fastapi.security.oauth2 import OAuth2PasswordBearer , OAuth2PasswordRequestForm   
from pydantic import BaseModel
import jwt 
from data.db_connection import get_db , users , verfiy_password
from datetime import datetime ,timedelta
from env import key , algorithm

time_to_expire = datetime.now() + timedelta(minutes= 10)

auth = OAuth2PasswordBearer("/user/login")


class Token(BaseModel):
    access_token : str
    token_type : str = "bearer"



def make_token(user : users = Depends(OAuth2PasswordRequestForm) , session : Session = Depends(get_db)) -> Token:
    try :
        query = session.exec(select(users).where(users.username == user.username)).one()
        query.is_active = True 
        session.add(query)
        session.commit()
        session.refresh(query)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if query.username == user.username:
        if verfiy_password(query.password, user.password) or query.password == user.password:
            token = jwt.encode(payload= {"username" : user.username,"exp": time_to_expire} , key=key , algorithm=algorithm )
            return Token(access_token=token)



def get_payload(token : str = Depends(auth), session : Session = Depends(get_db)) -> users:
    payload = jwt.decode( token, key,algorithm)
    if datetime.fromtimestamp(payload["exp"]) > datetime.now():
        try :
            query = session.exec(select(users).where(users.username == payload["username"])).one()
            if query.is_active:
                return query
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)




router = APIRouter()


@router.post("/signin")
def signin(user : users,session : Session = Depends(get_db)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return make_token(user,session)

@router.post("/login")
async def auth(token : Token = Depends(make_token)) -> Token:
    return token

@router.get("/logout")
async def logout(user : users = Depends(get_payload),session : Session = Depends(get_db)):
    user.is_active = False
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/delete_account")
async def delete_account(user : users = Depends(get_payload),session : Session = Depends(get_db)):
    session.delete(user)
    session.commit()
    return user


