from typing import Annotated
import uuid

from fastapi import FastAPI, Query, HTTPException
from sqlmodel import select

from .database import create_db_and_tables, SessionDep
from .models import Script, ScriptCreate, ScriptPublic, ScriptUpdate
from .models import TimerInterval, TimerTreePath, TimerIntervalCreate, TimerIntervalPublic, TimerIntervalUpdate

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

def add_timer(timer_interval: dict, script_id: uuid.UUID, session: SessionDep, ancestor_id: uuid.UUID=None, depth: int=0):
    timer = timer_interval["timer"]
    db_timer = TimerInterval.model_validate(TimerInterval(timer=timer, script_id=script_id))
    session.add(db_timer)
    session.commit()
    session.refresh(db_timer)

    if ancestor_id is not None:
        db_tree_path = TimerTreePath(ancestor_id=ancestor_id, descendant_id=db_timer.id, depth=depth)
        session.add(db_tree_path)
        session.commit()

    db_tree_path = TimerTreePath(ancestor_id=db_timer.id, descendant_id=db_timer.id, depth=0)
    session.add(db_tree_path)
    session.commit()

    if timer_interval["interval"] == []:
        return
    for interval in timer_interval["interval"]:
        add_timer(interval, script_id, session, ancestor_id=db_timer.id, depth=depth+1)

def get_timer_interval(script_id: uuid.UUID, session: SessionDep):
    root_timer = session.exec(select(TimerInterval).filter(TimerInterval.script_id == script_id)).first()
    if not root_timer:
        return None

    def get_interval(timer_id: uuid.UUID):
        timer_intervals =[]
        intervals = session.exec(select(TimerInterval).join(TimerTreePath, TimerTreePath.descendant_id == TimerInterval.id).filter(TimerTreePath.ancestor_id == timer_id, TimerTreePath.depth == 1)).all()

        for timer_interval in intervals:
            timer_intervals.append({
                "timer": timer_interval.timer,
                "interval": get_interval(timer_interval.id)
            })

        return timer_intervals

    return {
        "timer": root_timer.timer,
        "interval": get_interval(root_timer.id)
    }

# create a timer interval api
@app.post("/timer-intervals/{script_id}", response_model=TimerIntervalPublic)
def create_timer_interval(script_id: uuid.UUID, timer_interval: TimerIntervalCreate, session: SessionDep):
    timer_interval_data = timer_interval.model_dump()
    add_timer(timer_interval_data, script_id, session)
    return TimerIntervalPublic(**get_timer_interval(script_id, session))
