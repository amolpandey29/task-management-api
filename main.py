from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import get_connection
from task_repository import get_all_tasks, create_task, get_task, update_task, delete_task

app = FastAPI()


class TaskCreate(BaseModel):
    title: str
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


def get_db():
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()


@app.get("/")
def home():
    return {"message": "Task Management API is running"}


@app.get("/tasks")
def get_tasks(connection=Depends(get_db)):
    return get_all_tasks(connection)


@app.post("/tasks")
def create_tasks(task: TaskCreate, connection=Depends(get_db)):
    return create_task(connection, task.title, task.completed)


@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int, connection=Depends(get_db)):
    task = get_task(connection, task_id)
    if task is not None:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")


@app.patch("/tasks/{task_id}")
def update_task_by_id(
    task_id: int,
    task: TaskUpdate,
    connection=Depends(get_db)
):
    updated_task = update_task(
        connection,
        task_id,
        task.title,
        task.completed
    )

    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@app.delete("/tasks/{task_id}")
def delete_task_by_id(task_id: int, connection=Depends(get_db)):
    task_detail = delete_task(connection, task_id)

    if task_detail is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_detail
