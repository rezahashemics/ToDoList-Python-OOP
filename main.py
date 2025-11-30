from fastapi import FastAPI
# 💡 Import both routers
from src.api.v1.routers import projects, tasks 


app = FastAPI(
    title="ToDoList API",
    description="A RESTful API for managing ToDo Projects and Tasks.",
    version="1.0.0",
)

# 1. Include Routers (Controllers)
app.include_router(projects.router, prefix="/v1")
# 💡 شامل کردن router جدید تسک‌ها
app.include_router(tasks.router, prefix="/v1") 


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the ToDoList Web API! Go to /docs for documentation."}
