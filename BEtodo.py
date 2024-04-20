from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware import Middleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)


class Task(BaseModel):
    id: Optional[str] = None
    name: str
    isDone: bool = False


banco: List[Task] = []


@app.get("/")
def hello():
    return "Server is running!"


@app.get("/tasks")
def get_tasks():
    return banco


@app.get("/tasks/progress")
def get_tasks_progress():
    done = 0
    total = 0
    if len(banco) > 0:
        total = len(banco)
        for task in banco:
            if task.isDone == True:
                done += 1
    return {"done": done, "total": total}


@app.post("/tasks")
def create_task(newTask: Task):
    for task in banco:
        if task.name == newTask.name:
            return "A tarefa já existe!"
    newTask.id = str(uuid4())
    banco.append(newTask)
    return newTask


@app.delete("/tasks/{taskId}")
def delete_task(taskId: str):
    for task in banco:
        if task.id == taskId:
            banco.remove(task)
            return "Tarefa removida!"
    return "A tarefa não existe!"


@app.patch("/tasks/{taskId}")
def toggle_task_is_done(taskId: str):
    for task in banco:
        if task.id == taskId:
            if task.isDone == True:
                task.isDone = False
            else:
                task.isDone = True
            return task
    return "A tarefa não existe!"
