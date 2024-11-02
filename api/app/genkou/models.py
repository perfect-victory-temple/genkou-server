from datetime import datetime
import uuid
from typing import Optional

from sqlmodel import SQLModel, Field

# script model
class ScriptBase(SQLModel):
    title: str = Field(index=True)
    content: str
    timer: Optional[int] = Field(default=None)

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
    title: Optional[str] = None
    content: Optional[str] = None
    timer: Optional[int] = None