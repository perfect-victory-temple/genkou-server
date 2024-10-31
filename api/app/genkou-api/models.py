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