from sqlmodel import Field, SQLModel
from pydantic import field_validator, model_validator
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
  IN_PROGRESS = 'in-progress'
  SHELVED = 'shelved'
  COMPLETED = 'complete'
  


class TaskBase(SQLModel):
  title: str
  deadline: datetime | None
  status: TaskStatus | None = TaskStatus.SHELVED
  
class TaskCreate(TaskBase):
  
  @model_validator(mode="after")
  def validate_create_data(self):  
    self.title = self.title.strip()
    
    if self.deadline < datetime.now():
      raise ValueError("Deadline cannot be in the past")
  
    if not (8 <= len(self.title) <= 160) :
      raise ValueError("Title should have at least 8 characters and a maximum of 160 characters")

    if self.status == TaskStatus.COMPLETED:
      raise ValueError('Status cannot be "complete" when creating a task')
    

    
    return self
    
    
  

class Task(TaskBase, table = True):
  id: int | None = Field(primary_key=True, default = None)
  created_at: datetime | None = Field(default_factory=datetime.now)
  
