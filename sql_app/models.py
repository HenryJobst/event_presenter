import enum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Float, Double, Date
from sqlalchemy.orm import mapped_column, DeclarativeBase


# declarative base class
class Base(DeclarativeBase):
    pass


class EventStatus(enum.Enum):
    PLANNED = 'Planned'  # The event or race is on a planning stadium and has not been submitted to any sanctioning
    # body.
    APPLIED = 'Applied'  # The organiser has submitted the event to the relevant sanctioning body.
    PROPOSED = 'Proposed'  # The organiser has bid on hosting the event or race as e.g. a championship.
    SANCTIONED = 'Sanctioned'  # The event oc race meets the relevant requirements and will happen.
    CANCELED = 'Canceled'  # The event or race has been canceled, e.g. due to weather conditions.
    RESCHEDULED = 'Rescheduled'  # The date of the event or race has changed. A new Event or Race element should be
    # created in addition to the already existing element.


class EventClassification(enum.Enum):
    INTERNATIONAL = 'International'
    NATIONAL = 'National'
    REGIONAL = 'Regional'
    LOCAL = 'Local'
    CLUB = 'Club'


class EventForm(enum.Enum):
    INDIVIDUAL = 'Individual'
    TEAM = 'Team'
    RELAY = 'Relay'


class ResultListStatusType(enum.Enum):
    COMPLETE = 'Complete'  # The result list is complete, i.e. all competitors are included. Used for official
    # results after the event.
    DELTA = 'Delta'  # The result list only contains changes since last list. Used for frequent exchange of results.
    SNAPSHOT = 'Snapshot'  # The result list is a snapshot of the current standings. Used while the event is under way.

    @staticmethod
    def get_enum_value(value_string: str):
        if value_string == ResultListStatusType.COMPLETE.value:
            return ResultListStatusType.COMPLETE
        elif value_string == ResultListStatusType.DELTA.value:
            return ResultListStatusType.DELTA
        elif value_string == ResultListStatusType.SNAPSHOT.value:
            return ResultListStatusType.SNAPSHOT
        else:
            raise ValueError('Invalid enum value: {}'.format(value_string))


class Organisation(Base):
    __tablename__ = "organisations"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, index=True, nullable=False)
    short_name = mapped_column(String(20))


class Event(Base):
    __tablename__ = "events"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, index=True, nullable=False)
    status = mapped_column(Enum(EventStatus))
    classification = mapped_column(Enum(EventClassification))
    form = mapped_column(Enum(EventForm))
    organisation = mapped_column(Integer, ForeignKey("organisations.id"))


class ResultList(Base):
    __tablename__ = "result_lists"

    id = mapped_column(Integer, primary_key=True, index=True)
    event = mapped_column(Integer, ForeignKey("events.id"))
    status = mapped_column(Enum(ResultListStatusType))
    create_time = mapped_column(DateTime)
    creator = mapped_column(String)

    # class_results = relationship("ClassResult", back_populates="result_list")


class ResultListModeType(enum.Enum):
    DEFAULT = 'Default'  # The result list should include place and time for each competitor, and be ordered by place.
    UNORDERED = 'Unordered'  # The result list should include place and time for each competitor, but be unordered
    # with respect to times (e.g. sorted by competitor name).
    UNORDERED_NO_TIMES = 'UnorderedNoTimes'  # The result list should not include any places and times,

    # and be unordered with respect to times (e.g. sorted by competitor name).

    @staticmethod
    def get_enum_value(value_string: str):
        if value_string == ResultListModeType.DEFAULT.value:
            return ResultListModeType.DEFAULT
        elif value_string == ResultListModeType.UNORDERED.value:
            return ResultListModeType.UNORDERED
        elif value_string == ResultListModeType.UNORDERED_NO_TIMES.value:
            return ResultListModeType.UNORDERED_NO_TIMES
        else:
            raise ValueError('Invalid enum value: {}'.format(value_string))


class SexType(enum.Enum):
    F = 'F'
    M = 'M'

    @staticmethod
    def get_enum_value(value_string: str):
        if value_string == SexType.F.value:
            return SexType.F
        elif value_string == SexType.M.value:
            return SexType.M
        else:
            raise ValueError('Invalid enum value: {}'.format(value_string))


class EventClassStatus(enum.Enum):
    NORMAL = 'Normal'  # The default status.
    DIVIDED = 'Divided'  # The class has been divided in two or more classes due to a large number of entries.
    JOINED = 'Joined'  # The class has been joined with another class due to a small number of entries.
    INVALIDATED = 'Invalidated'  # The results are considered invalid due to technical issues such as misplaced
    # controls. Entry fees are not refunded.
    INVALIDATED_NO_FEE = 'InvalidatedNoFee'  # The results are considered invalid due to technical issues such as

    # misplaced controls. Entry fees are refunded.

    @staticmethod
    def get_enum_value(value_string: str):
        if value_string == EventClassStatus.NORMAL.value:
            return EventClassStatus.NORMAL
        elif value_string == EventClassStatus.DIVIDED.value:
            return EventClassStatus.DIVIDED
        elif value_string == EventClassStatus.JOINED.value:
            return EventClassStatus.JOINED
        elif value_string == EventClassStatus.INVALIDATED.value:
            return EventClassStatus.INVALIDATED
        elif value_string == EventClassStatus.INVALIDATED_NO_FEE.value:
            return EventClassStatus.INVALIDATED_NO_FEE
        else:
            raise ValueError('Invalid enum value: {}'.format(value_string))


class EventClass(Base):
    __tablename__ = "event_classes"

    id = mapped_column(Integer, primary_key=True, index=True, nullable=True)
    result_list = mapped_column(Integer, ForeignKey("result_lists.id"))
    name = mapped_column(String)
    short_name = mapped_column(String, nullable=True)
    result_list_mode = mapped_column(Enum(ResultListModeType))
    status = mapped_column(Enum(EventClassStatus))
    sex = mapped_column(Enum(SexType))
    min_number_of_team_members = mapped_column(Integer, default=1)
    max_number_of_team_members = mapped_column(Integer, default=1)


class Course(Base):
    __tablename__ = "courses"

    id = mapped_column(Integer, primary_key=True, index=True)
    result_list = mapped_column(Integer, ForeignKey("result_lists.id"))
    event_class = mapped_column(Integer, ForeignKey("event_classes.id"))
    race_number = mapped_column(Integer, default=1)
    name = mapped_column(String, nullable=True)
    course_id = mapped_column(String, nullable=True)
    course_family = mapped_column(String, nullable=True)
    length = mapped_column(Double, nullable=True)
    climb = mapped_column(Double, nullable=True)
    number_of_controls = mapped_column(Integer, nullable=True)


class ClassResult(Base):
    __tablename__ = "class_results"

    id = mapped_column(Integer, primary_key=True, index=True)
    time_resolution = mapped_column(Float, nullable=False)
    event_class = Column(Integer, ForeignKey("event_classes.id"))
    result_list = Column(Integer, ForeignKey("result_lists.id"))


class Person(Base):
    __tablename__ = "persons"

    id = mapped_column(Integer, primary_key=True, index=True)
    sex = mapped_column(Enum(SexType))
    family_name = mapped_column(String)
    given_name = mapped_column(String)
    birth_date = mapped_column(Date)


class PersonResult(Base):
    __tablename__ = "person_results"

    id = mapped_column(Integer, primary_key=True, index=True)
    person = mapped_column(Integer, ForeignKey("persons.id"))
    organisation = mapped_column(Integer, ForeignKey("organisations.id"), nullable=True)


class ResultStatus(enum.Enum):
    OK = 'OK'  # Finished and validated.
    FINISHED = 'Finished'  # Finished but not yet validated.
    MISSING_PUNCH = 'MissingPunch'  # Missing punch.
    DISQUALIFIED = 'Disqualified'  # Disqualified (for some other reason than a missing punch).
    DID_NOT_FINISH = 'DidNotFinish'  # Did not finish (i.e. conciously cancelling the race after having started,
    # in contrast to MissingPunch).
    ACTIVE = 'Active'  # Currently on course.
    INACTIVE = 'Inactive'  # Has not yet started.
    OVER_TIME = 'OverTime'  # Overtime, i.e. did not finish within the maximum time set by the organiser.
    SPORTING_WITHDRAWAL = 'SportingWithdrawal'  # Sporting withdrawal (e.g. helping an injured competitor).
    NOT_COMPETING = 'NotCompeting'  # Not competing (i.e. running outside the competition).
    MOVED = 'Moved'  # Moved to another class.
    MOVED_UP = 'MovedUp'  # Moved to a "better" class, in case of entry restrictions.
    DID_NOT_START = 'DidNotStart'  # Did not start (in this race).
    DID_NOT_ENTER = 'DidNotEnter'  # Did not enter (in this race).
    CANCELLED = 'Cancelled'  # The competitor has cancelled his/hers entry.


class PersonRaceResult(Base):
    __tablename__ = "person_race_results"

    id = mapped_column(Integer, primary_key=True, index=True)
    bib_number = mapped_column(String, nullable=True)
    start_time = mapped_column(DateTime, nullable=True)
    finish_time = mapped_column(DateTime, nullable=True)
    time = mapped_column(Double, nullable=True)
    time_behind = mapped_column(Double, nullable=True)
    position = mapped_column(Integer, nullable=True)
    status = mapped_column(Enum(ResultStatus))
    control_card = mapped_column(String, nullable=True)


class SplitTimeStatusType(enum.Enum):
    OK = 'OK'  # Control belongs to the course and has been punched (either by electronical punching or pin
    # punching). If the time is not available or invalid, omit the Time element.
    MISSING = 'Missing'  # Control belongs to the course but has not been punched.
    ADDITIONAL = 'Additional'  # Control does not belong to the course, but the competitor has punched it.


class SplitTime(Base):
    __tablename__ = "split_times"

    id = mapped_column(Integer, primary_key=True, index=True)
    result = mapped_column(Integer, ForeignKey("person_race_results.id"))
    status = mapped_column(Enum(SplitTimeStatusType), default=SplitTimeStatusType.OK)
    control_code = mapped_column(String)
    time = mapped_column(Double, nullable=True)
