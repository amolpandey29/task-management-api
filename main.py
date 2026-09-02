from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection

app = FastAPI()

class TaskCreate(BaseModel):
	title: str
	completed: bool = False

class TaskUpdate(BaseModel):
	title: str | None = None
	completed: bool | None = None

tasks = [
	{
		"id": 1,
		"title": "Learn FastAPI",
		"completed": False
	},
	{
		"id": 2,
		"title": "Learn SQL",
		"completed": False
	},
]

@app.get("/")
def home():
	return {"message" : "Task Management API is running"}

@app.get("/tasks")
def get_tasks():
	connection = get_connection()
	cursor = connection.cursor(dictionary=True)

	cursor.execute("SELECT * FROM tasks")
	tasks = cursor.fetchall()

	cursor.close()
	connection.close()

	return tasks

@app.post("/tasks")
def create_tasks(task: TaskCreate):
	connection = get_connection()
	cursor = connection.cursor(dictionary=True)
	
	cursor.execute("INSERT INTO tasks(title, completed) VALUES (%s,%s)",(task.title, task.completed))
	connection.commit()

	last_row_id = cursor.lastrowid
	cursor.execute("SELECT * FROM tasks WHERE id = %s",(last_row_id,))
	new_task = cursor.fetchone()

	cursor.close()
	connection.close()

	return new_task

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
	connection = get_connection()
	cursor = connection.cursor(dictionary=True)

	cursor.execute("SELECT * FROM tasks WHERE id = %s",(task_id,))
	task = cursor.fetchone()

	cursor.close()
	connection.close()

	if task is not None:
		return task
	else:
		raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    existing_task = cursor.fetchone()

    if existing_task is None:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Task not found")

    if task.title is not None and task.completed is not None:
        cursor.execute(
            "UPDATE tasks SET title = %s, completed = %s WHERE id = %s",
            (task.title, task.completed, task_id)
        )
        connection.commit()

    elif task.title is not None:
        cursor.execute(
            "UPDATE tasks SET title = %s WHERE id = %s",
            (task.title, task_id)
        )
        connection.commit()

    elif task.completed is not None:
        cursor.execute(
            "UPDATE tasks SET completed = %s WHERE id = %s",
            (task.completed, task_id)
        )
        connection.commit()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    updated_task = cursor.fetchone()

    cursor.close()
    connection.close()

    return updated_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    existing_task = cursor.fetchone()

    if existing_task is None:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "Task deleted"}
