import datetime

from pydantic import BaseModel

from sql_app.models import ResultListStatusType, ResultListModeType, EventClassStatus, SexType


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

class EventClassBase(BaseModel):
    name: str
    short_name: str = None
    sex: SexType
    result_list_mode: ResultListModeType = ResultListModeType.DEFAULT
    status: EventClassStatus = EventClassStatus.NORMAL
    min_number_of_team_members: int = 1
    max_number_of_team_members: int = 1
    result_list: int


class EventClassCreate(EventClassBase):
    pass