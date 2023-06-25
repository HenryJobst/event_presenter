import datetime

from pydantic import BaseModel

from sql_app.models import ResultListStatusType


class EventBase(BaseModel):
    name: str
    status: str = None
    classification: str = None
    form: str = None
    organisation: str = None


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int

    class Config:
        orm_mode = True


class ResultListBase(BaseModel):
    status: ResultListStatusType
    create_time: datetime.datetime
    creator: str
    event: Event


class ResultListCreate(ResultListBase):
    pass


class ResultList(ResultListBase):
    id: int

    class Config:
        orm_mode = True
