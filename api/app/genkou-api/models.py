from datetime import datetime
import uuid

from sqlmodel import SQLModel, Field

# script model
class ScriptBase(SQLModel):
    title: str = Field(index=True)
    content: str
    timer: int | None = Field(default=None)

class Script(ScriptBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, index=True)
    updated_at: datetime = Field(default_factory=datetime.now, index=True)

class ScriptPublic(ScriptBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class ScriptCreate(ScriptBase):
    pass

class ScriptUpdate(ScriptBase):
    title: str | None = None
    content: str | None = None
    timer: int | None = None

# timer_interval model
class TimerIntervalBase(SQLModel):
    timer: int

class TimerInterval(TimerIntervalBase, table=True):
    script_id: uuid.UUID
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class TimerTreePath(SQLModel, table=True):
    ancestor_id: uuid.UUID = Field(primary_key=True)
    descendant_id: uuid.UUID = Field(primary_key=True)
    depth: int

class TimerIntervalCreate(TimerIntervalBase):
    interval: list['TimerIntervalCreate'] = []

class TimerIntervalPublic(TimerIntervalBase):
    timer: int | None
    interval: list['TimerIntervalPublic'] = []

class TimerIntervalUpdate(TimerIntervalBase):
    timer: int | None = None
    interval: list['TimerIntervalUpdate'] = []