from fastapi import FastAPI

from app.routers.task_router import router as task_router
from app.infrastructure.database import Base, engine
from app.infrastructure.db_models import TaskModel

#Create table at startup
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(task_router)

@app.get("/")
def root():
    return {"message": "API Tasks OK"}