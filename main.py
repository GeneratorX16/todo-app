from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from db import init_db, SessionDep
from models import Task, TaskBase, TaskCreate, TaskStatus

from sqlmodel import select, col

@asynccontextmanager
async def startup(app: FastAPI):
  init_db()
  yield
  
app = FastAPI(lifespan=startup)


@app.get("/")
async def root() -> dict:
  return {
    "message": "Manage all your tasks over here"
  }
  
@app.get('/tasks')
async def get_tasks(session: SessionDep, q: str | None = None, status: TaskStatus | None = None) -> list[Task]:
  query = select(Task)
  
  if q is not None:
    query = query.where(col(Task.title).contains(q))
  
  if status:
    query = query.where(Task.status == status)
  results = session.exec(query)
  return results

@app.post("/task")
async def create_task(task: TaskCreate, session: SessionDep) -> Task:
  task_instance = Task.model_validate(task)
  session.add(task_instance)
  session.commit()
  session.refresh(task_instance)
  return task_instance

@app.delete("/task/{id}", status_code=204)
async def delete_task(id: int, session: SessionDep):
  task_instance = session.get(Task, id)
  
  if task_instance is None:
    raise HTTPException(status_code=404, detail = "Resource does not  exist")
  
  session.delete(task_instance)
  session.commit()
  
  
