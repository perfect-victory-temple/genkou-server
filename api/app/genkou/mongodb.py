from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from motor.motor_asyncio import AsyncIOMotorClient

from .config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client.genkou
timer_collection = db.get_collection("timer")

# convert ObjectIds to str before storing them as the id field
# # MongoDB stores data as BSON. FastAPI encodes and decodes data as JSON strings.
# # BSON has support for additional non-JSON-native data types like ObjectId.
PyObjectId = Annotated[str, BeforeValidator(str)]

# Timer model
class TimerInterval(BaseModel):
    timer: int = Field(gt=0)
    intervals: list['TimerInterval'] = []

class TimerBase(BaseModel):
    timer_interval: TimerInterval
    # model_config = ConfigDict(
    #     arbitrary_types_allowed=True
    # )

class TimerCreate(TimerBase):
    pass

class TimerPublic(TimerBase):
    id: PyObjectId = Field(alias="_id")
    model_config = ConfigDict(
        populate_by_name=True
    )

class TimerUpdate(TimerBase):
    timer_interval: TimerInterval | None = None