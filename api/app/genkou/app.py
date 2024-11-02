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
    limit: Annotated[int, Query(le=10)] = 10,  # limit <= 10
):
    scripts = session.exec(select(Script).offset(offset).limit(limit)).all()
    return scripts

# update a script api
@app.put("/scripts/{script_id}", response_model=ScriptPublic)
def update_script(script_id: uuid.UUID, script: ScriptUpdate, session: SessionDep):
    db_script = session.get(Script, script_id)
    if not db_script:
        raise HTTPException(status_code=404, detail="Script not found")
    script_data = script.model_dump(exclude_unset=True)  # get only the data sent by the client
    if not script_data:
        return db_script
    db_script.sqlmodel_update(script_data)
    session.add(db_script)
    session.commit()
    session.refresh(db_script)
    return db_script

# delete a script api
@app.delete("/scripts/{script_id}")
def delete_script(script_id: uuid.UUID, session: SessionDep):
    script = session.get(Script, script_id)
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    session.delete(script)
    session.commit()
    return {"ok": True}

from .mongodb import TimerCreate, TimerPublic, TimerUpdate
from .mongodb import timer_collection
from bson import ObjectId

# post a timer api
@app.post("/timers/", response_model=TimerPublic)
async def create_timer(timer: TimerCreate):
    timer_data = timer.model_dump()
    new_timer = await timer_collection.insert_one(timer_data)
    created_timer = await timer_collection.find_one({"_id": new_timer.inserted_id})

    return created_timer

# get a timer api
@app.get("/timers/{timer_id}", response_model=TimerPublic)
async def read_timer(timer_id: str):
    try:
        object_id = ObjectId(timer_id)
    except:
        raise HTTPException(status_code=404, detail=f"Timer {timer_id} not found")

    timer = await timer_collection.find_one({"_id": object_id})
    if timer:
        return timer

    raise HTTPException(status_code=404, detail=f"Timer {timer_id} not found")

# update a timer api
@app.put("/timers/{timer_id}", response_model=TimerPublic)
async def update_timer(timer_id: str, timer: TimerUpdate):
    try:
        object_id = ObjectId(timer_id)
    except:
        raise HTTPException(status_code=404, detail=f"Timer {timer_id} not found")
    timer_data = timer.model_dump(exclude_unset=True)
    if not timer_data:
        existing_timer = await timer_collection.find_one({"_id": object_id})
        return existing_timer

    updated_result = await timer_collection.replace_one({"_id": object_id}, timer_data)
    if updated_result.modified_count:
        updated_timer = await timer_collection.find_one({"_id": object_id})
        return updated_timer

    raise HTTPException(status_code=404, detail=f"Timer {timer_id} not found")

# delete a timer api
@app.delete("/timers/{timer_id}")
async def delete_timer(timer_id: str):
    try:
        object_id = ObjectId(timer_id)
    except:
        raise HTTPException(status_code=404, detail=f"Timer {timer_id} not found")

    delete_result = await timer_collection.delete_one({"_id": object_id})
    if delete_result.deleted_count == 1:
        return {"ok": True}

    raise HTTPException(status_code=404, detail=f"Timer {timer_id} not found")