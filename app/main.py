from fastapi import FastAPI

from app.routers.task_router import router as task_router
from app.routers.task_router import router as auth_router
from app.infrastructure.database import Base, engine
from app.infrastructure.models import UserModel, RefreshTokenModel, TaskModel

#Create table at startup
#This line is redundant due to Alembic
#Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(task_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "API Tasks OK"}