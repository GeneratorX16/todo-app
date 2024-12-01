from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends
from typing import Annotated


db_file_name = 'mydb.db'
sqlite_url = f'sqlite:///{db_file_name}'

db_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args = db_args)


def init_db():
  SQLModel.metadata.create_all(engine)
  
def get_session():
  with Session(engine) as session:
    yield session
    
    
SessionDep = Annotated[Session, Depends(get_session)]

    
    