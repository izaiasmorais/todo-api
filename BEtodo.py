from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware import Middleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=[""],
        allow_credentials=True,
        allow_methods=[""],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)


class Task(BaseModel):
    id: Optional[str] = None
    name: str
    is_done: bool = False


banco: List[Task] = []


@app.get("/")
def hello_world():
    return "fala, izaias! bem vindo ao Back end do to-do!"


@app.get("/tasks")
def get_tasks():
    return banco


@app.get("/tasks/progress")
def get_task_progress():
    done = 0
    total = 0
    if len(banco) > 0:
        total = len(banco)
        for task in banco:
            if task.is_done == True:
                done += 1
    return {"done": done, "total": total}


@app.post("/task")
def create_task(new_task: Task):
    for task in banco:
        if task.name == new_task.name:
            return "A tarefa já existe!"
    new_task.id = str(uuid4())
    banco.append(new_task)
    return new_task


@app.get("/task/{task_id}")
def get_task_by_id(task_id: str):
    for task in banco:
        if task.id == task_id:
            return task
    return "A tarefa não existe!"


@app.delete("/task/{task_id}")
def delete_task(task_id: str):
    for task in banco:
        if task.id == task_id:
            banco.remove(task)
            return "tarefa removida!"
    return "A tarefa não existe!"


@app.put("/task/{task_id}")
def toggle_task_is_done(task_id: str):
    for task in banco:
        if task.id == task_id:
            if task.is_done == True:
                task.is_done = False
            else:
                task.is_done = True
            return task
        else:
            return "A tarefa não existe!"

