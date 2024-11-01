from typing import Annotated

from pydantic import BeforeValidator
from motor.motor_asyncio import AsyncIOMotorClient

from .config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client.genkou
timer_collection = db.get_collection("timer")

# convert ObjectIds to str before storing them as the id field
# # MongoDB stores data as BSON. FastAPI encodes and decodes data as JSON strings.
# # BSON has support for additional non-JSON-native data types like ObjectId.
PyObjectId = Annotated[str, BeforeValidator(str)]