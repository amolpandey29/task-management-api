from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
	title: str
	completed: bool = False

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
	return tasks

@app.post("/tasks")
def create_tasks(task: TaskCreate):
	new_task = {
		"id": len(tasks)+1,
		"title": task.title,
		"completed": task.completed
	}
	tasks.append(new_task);
	return tasks