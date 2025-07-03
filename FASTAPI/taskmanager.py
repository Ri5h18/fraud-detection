from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
tasks = []
task_id_counter = 1

class Task(BaseModel):
    title: str
    description: str = ""
    completed: bool = False

@app.post("/tasks/")
def create_task(task: Task):
    global task_id_counter
    task_dict = task.dict()
    task_dict["id"] = task_id_counter
    tasks.append(task_dict)
    task_id_counter += 1
    return task_dict

@app.get("/tasks/")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            return tasks.pop(i)
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return task
    raise HTTPException(status_code=404, detail="Task not found")
