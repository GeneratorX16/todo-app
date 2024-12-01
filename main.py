from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from db import init_db, SessionDep
from models import Task, TaskUpdate, TaskCreate, TaskStatus, datetime

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
async def get_tasks(
  session: SessionDep, q: str | None = None, status: TaskStatus | None = None,
  created_before: datetime | None = None, created_after: datetime | None = None,
  deadline_before: datetime | None = None, deadline_after: datetime | None = None) -> list[Task]:
  query = select(Task)
  
  if q is not None:
    query = query.where(col(Task.title).contains(q))
  
  if status is not None:
    query = query.where(Task.status == status)
  
  if created_before is not None:
    query = query.where(Task.created_at < created_before)
    
  if created_after is not None:
    query = query.where(Task.created_at > created_after)
  
  if deadline_after is not None:
    query = query.where(Task.deadline > deadline_after)
    
  if deadline_before is not None:
    query = query.where(Task.deadline < deadline_before)
    
    
  results = session.exec(query)
  return results

@app.post("/task", status_code=201)
async def create_task(task: TaskCreate, session: SessionDep) -> Task:
  task_instance = Task.model_validate(task)
  session.add(task_instance)
  session.commit()
  session.refresh(task_instance)
  return task_instance

@app.put("/task/{id}")
async def update_task(id: int, task: TaskUpdate,session: SessionDep) -> Task:
  task_instance = session.get(Task, id)
  
  if task_instance is None: raise HTTPException(status_code=404, detail = "Resource does not  exist")
  
  # validation for updating task after pydantic validation
  if task_instance.status == TaskStatus.COMPLETED:  raise HTTPException(status_code=400, detail="A completed task cannot be updated")
  
  updated_task_data = task.model_dump(exclude_unset=True)
  task_instance.sqlmodel_update(updated_task_data)
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
  
  
