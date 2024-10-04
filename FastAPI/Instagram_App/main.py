from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from end_points import user , post , comment 
from contextlib import  asynccontextmanager
from data.db_connection import map_tables , redis_db



@asynccontextmanager
async def start_end(app : FastAPI):
    redis_db.set("image_counter",0)
    map_tables()
    yield 


app = FastAPI(lifespan=start_end)

app.include_router(router=user.router,prefix="/user",tags=["user"])
app.include_router(router=post.router,prefix="/post",tags=["post"])
app.include_router(router=comment.router,prefix="/comment",tags=["comment"])

app.mount(path="/images",app=StaticFiles(directory ="images"), name= "images")


