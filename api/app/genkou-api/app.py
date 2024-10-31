from typing import Annotated

from fastapi import FastAPI, Query
from sqlmodel import select

from .database import create_db_and_tables, SessionDep
from .models import Script, ScriptCreate, ScriptPublic

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# create a script api
@app.post("/scripts/", response_model=ScriptPublic)
def create_script(script: ScriptCreate, session: SessionDep):
    db_script = Script.model_validate(script)
    session.add(db_script)
    session.commit()
    session.refresh(db_script)
    return db_script