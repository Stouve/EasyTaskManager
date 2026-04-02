from fastapi import FastAPI
from app.routers.task_router import router as task_router

app = FastAPI()
app.include_router(task_router)

@app.get("/")
def root():
    return {"message": "API Tasks OK"}