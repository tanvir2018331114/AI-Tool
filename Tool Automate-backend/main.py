import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from agent import execute_workflow
from models import Tool
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Tool Automator API"}

@app.post("/register_tool")
def register_tool(tool: schemas.ToolCreate, db: Session = Depends(get_db)):
    db_tool = Tool(**tool.dict())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return {"message": "Tool registered"}

@app.post("/run_task")
def run_task(task_input: schemas.TaskRequest, db: Session = Depends(get_db)):
    trace = execute_workflow(task_input.task, db)
    return {"trace": trace}
