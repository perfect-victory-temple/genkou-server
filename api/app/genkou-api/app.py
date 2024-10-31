from typing import Annotated
import uuid

from fastapi import FastAPI, Query, HTTPException
from sqlmodel import select

from .database import create_db_and_tables, SessionDep
from .models import Script, ScriptCreate, ScriptPublic, ScriptUpdate

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

# read scripts api
@app.get("/scripts/", response_model=list[ScriptPublic])
def read_scripts(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=10)] = 10, # limit <= 10
):
    scripts = session.exec(select(Script).offset(offset).limit(limit)).all()
    return scripts

# update a script api
@app.put("/scripts/{script_id}", response_model=ScriptPublic)
def update_script(script_id: uuid.UUID, script: ScriptUpdate, session: SessionDep):
    db_script = session.get(Script, script_id)
    if not db_script:
        raise HTTPException(status_code=404, detail="Script not found")
    script_data = script.model_dump(exclude_unset=True) # get only the data sent by the client
    if not script_data:
        return db_script
    db_script.sqlmodel_update(script_data)
    session.add(db_script)
    session.commit()
    session.refresh(db_script)
    return db_script