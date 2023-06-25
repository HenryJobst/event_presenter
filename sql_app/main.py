from fastapi import FastAPI, HTTPException, Depends

from . import schemas, crud
from .database import SessionLocal
from sqlalchemy.orm import Session

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = crud.get_event_by_name(db, name=event.name)
    if db_event:
        raise HTTPException(status_code=400, detail="Event already registered")
    return crud.create_event(db=db, event=event)


@app.get("/events/", response_model=list[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events


@app.get("/result_lists/", response_model=list[schemas.ResultList])
def read_result_lists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result_lists = crud.get_result_lists(db, skip=skip, limit=limit)
    return result_lists
