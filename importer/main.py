import datetime

import lxml.etree as et
import typer
from sqlalchemy.orm import Session
from xmlschema import XMLSchema

from sql_app.crud import find_or_create_event, find_or_create_result_list
from sql_app.database import SessionLocal
from sql_app.models import Event, ResultList, ResultListStatusType

app = typer.Typer()


def import_event(data: dict, db: Session):
    return find_or_create_event(db, data['Name'])


def import_result_list(data: dict, db: Session):
    event: Event = import_event(data['Event'], db)
    create_time = datetime.datetime.strptime(data['@createTime'], '%Y-%m-%dT%H:%M:%S.%f')
    status = ResultListStatusType.get_enum_value(data['@status'])
    result_list: ResultList = find_or_create_result_list(
        db=db, event=event,
        status=status,
        creator=data['@creator'],
        create_time=create_time)
    import_class_results(data['ClassResult'], event, result_list, db)


def import_dict(data: dict):
    import_result_list(data, SessionLocal())


def import_class_results(data: dict, event: Event, result_list: ResultList, db: Session):
    # print(json.dumps(data, indent=2))
    for class_result in data:
        import_class_result(class_result, event, result_list, db)


def import_event_class(data: dict):
    pass


def import_course(data: dict):
    pass


def import_person_race_results(
        data: dict,
        event_class,
        course,
        db: Session):
    pass


def import_class_result(data: dict, event: Event, result_list: ResultList, db: Session):
    event_class = import_event_class(data['Class'])
    course = import_course(data['Course'])
    import_person_race_results(
        data['PersonResult'],
        event_class,
        course,
        db)


@app.command()
def init(filename: str, schema: str = "./importer/data/IOF.xsd"):
    print(f"Init with {filename}")

    schema: XMLSchema = XMLSchema(schema)
    xt = et.parse(filename)

    print(f"Schema is valid: {schema.is_valid(xt)}")

    as_dict = schema.to_dict(xt, decimal_type=str)

    import_dict(as_dict)


if __name__ == "__main__":
    app()
