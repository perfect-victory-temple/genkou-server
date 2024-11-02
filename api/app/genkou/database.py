from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from .config import POSTGRES_URI

# create an engine
# a SQLModel engine is what holds the connections to the database
engine = create_engine(POSTGRES_URI)

# create the tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# create a Session Dependency
# a Session is what stores the objects in memory
#   and keeps track of any changes needed in the data
def get_session():
    with Session(engine) as session:
        yield session

# provide a new Session for each request
# this is what ensures that we use a single session per request

SessionDep = Annotated[Session, Depends(get_session)]