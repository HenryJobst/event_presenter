import datetime
from typing import Optional

from sqlalchemy.orm import Session

from . import models, schemas
from .models import Event, ResultList, ResultListStatusType
from .schemas import EventCreate, ResultListCreate


def get_event(db: Session, event_id: int) -> Optional[Event]:
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def get_event_by_name(db: Session, name: str) -> Optional[Event]:
    return db.query(models.Event).filter(models.Event.name == name).first()


def find_or_create_event(db: Session, name: str) -> Optional[Event]:
    event = get_event_by_name(db, name)
    if event:
        return event
    return create_event(db, EventCreate(name=name))


def create_event(db: Session, event: schemas.EventCreate) -> Event:
    db_event = models.Event(name=event.name, status=event.status, classification=event.classification,
                            form=event.form, organisation=event.organisation)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_result_list(db: Session, result_list_id: int) -> Optional[ResultList]:
    return db.query(models.ResultList).filter(models.ResultList.id == result_list_id).first()


def get_result_lists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ResultList).offset(skip).limit(limit).all()


def get_result_list_by_event_creator_creation_time(
        db: Session, event: Event, creator: str, create_time: datetime.datetime) -> Optional[ResultList]:
    return db.query(models.ResultList).filter(models.ResultList.event == event.id and models.ResultList.creator ==
                                              creator and models.ResultList.create_time == create_time
                                              ).first()


def find_or_create_result_list(db: Session, event: Event, status: ResultListStatusType, creator: str,
                               create_time: datetime.datetime) -> Optional[ResultList]:
    result_list = get_result_list_by_event_creator_creation_time(db, event, creator, create_time)
    if result_list:
        return result_list
    result_list_create = ResultListCreate(event=event, status=status, creator=creator, create_time=create_time)
    return create_result_list(db, result_list_create)


def create_result_list(db: Session,
                       result_list: schemas.ResultListCreate) -> ResultList:
    db_result_list = models.ResultList(
        event=result_list.event.id, status=result_list.status,
        creator=result_list.creator,
        create_time=result_list.create_time)
    db.add(db_result_list)
    db.commit()
    db.refresh(db_result_list)
    return db_result_list
