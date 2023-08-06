from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, Union

from ssb_altinn3_util.database import schema
from ssb_altinn3_util.models.altinn3_cloud_event import Altinn3CloudEvent


def add_altinn_event(db: Session, event: Altinn3CloudEvent) -> schema.AltinnEvent:
    db_event: schema.AltinnEvent = schema.AltinnEvent(**event.dict())
    db.add(db_event)
    db.flush()
    db.refresh(db_event)
    process = schema.AltinnEventProcess(
        event_id=db_event.db_id, received_at=datetime.utcnow()
    )
    db.add(process)
    db.commit()
    db.refresh(db_event)
    return db_event


def add_altinn_event_data(
    db: Session, instance: str, data_url: str, event_db_id: int
) -> schema.AltinnEventData:
    event_data: schema.AltinnEventData = schema.AltinnEventData(
        event_id=event_db_id, instance=instance, data_base_url=data_url
    )
    db.add(event_data)
    db.commit()
    db.refresh(event_data)
    return event_data


def update_event_data(
    db: Session,
    event_db_id: int,
    instance: Optional[str] = None,
    data_url: Optional[str] = None,
) -> schema.AltinnEventData:
    event_data: schema.AltinnEventData = (
        db.query(schema.AltinnEventData)
        .filter(schema.AltinnEventData.event_id == event_db_id)
        .first()
    )
    if not event_data:
        raise ValueError(f"EventData with id: '{event_db_id}' not found.")
    event_data.instance = event_data.instance if not instance else instance
    event_data.data_base_url = event_data.data_base_url if not data_url else data_url
    db.commit()
    db.refresh(event_data)
    return event_data


def update_progress(
    db: Session,
    event_db_id: int,
    data_fetched_at: Optional[datetime] = None,
    confirmed_altinn_at: Optional[datetime] = None,
    confirmed_ssb_at: Optional[datetime] = None,
    shared_at: Optional[datetime] = None,
    deadlettered: Optional[datetime] = None,
) -> schema.AltinnEventProcess:
    process: schema.AltinnEventProcess = (
        db.query(schema.AltinnEventProcess)
        .filter(schema.AltinnEventProcess.event_id == event_db_id)
        .first()
    )
    if not process:
        raise ValueError(f"EventProcess with id: '{event_db_id}' not found.")
    process.data_fetched_at = _get_value_if_updated(
        process.data_fetched_at, data_fetched_at
    )
    process.confirmed_altinn_at = _get_value_if_updated(
        process.confirmed_altinn_at, confirmed_altinn_at
    )
    process.confirmed_ssb_at = _get_value_if_updated(
        process.confirmed_ssb_at, confirmed_ssb_at
    )
    process.shared_at = _get_value_if_updated(process.shared_at, shared_at)
    process.deadlettered = _get_value_if_updated(process.deadlettered, deadlettered)

    db.commit()
    db.refresh(process)
    return process


def get_event_by_id(db: Session, event_id: str) -> schema.AltinnEvent:
    event: schema.AltinnEvent = (
        db.query(schema.AltinnEvent).filter(schema.AltinnEvent.id == event_id).first()
    )
    return event


def get_event_by_db_id(db: Session, db_id: int) -> schema.AltinnEvent:
    event: schema.AltinnEvent = (
        db.query(schema.AltinnEvent).filter(schema.AltinnEvent.db_id == db_id).first()
    )
    return event


def get_event_process_by_event_id(
    db: Session, event_id: str
) -> schema.AltinnEventProcess:
    process: schema.AltinnEventProcess = (
        db.query(schema.AltinnEvent)
        .filter(schema.AltinnEvent.id == event_id)
        .first()
        .process
    )
    return process


def get_event_process_by_event_db_id(
    db: Session, event_db_id: int
) -> schema.AltinnEventProcess:
    process: schema.AltinnEventProcess = (
        db.query(schema.AltinnEventProcess)
        .filter(schema.AltinnEventProcess.event_id == event_db_id)
        .first()
    )
    return process


def get_event_process_by_db_id(db: Session, db_id: int) -> schema.AltinnEventProcess:
    process: schema.AltinnEventProcess = (
        db.query(schema.AltinnEventProcess)
        .filter(schema.AltinnEventProcess.id == db_id)
        .first()
    )
    return process


def get_event_data_by_event_id(db: Session, event_id: str) -> schema.AltinnEventData:
    event_data: schema.AltinnEventData = (
        db.query(schema.AltinnEvent)
        .filter(schema.AltinnEvent.id == event_id)
        .first()
        .event_data
    )
    return event_data


def get_event_data_by_event_db_id(
    db: Session, event_db_id: int
) -> schema.AltinnEventData:
    event_data: schema.AltinnEventData = (
        db.query(schema.AltinnEventData)
        .filter(schema.AltinnEventData.event_id == event_db_id)
        .first()
    )
    return event_data


def get_event_data_by_db_id(db: Session, db_id: int) -> schema.AltinnEventData:
    event_data: schema.AltinnEventData = (
        db.query(schema.AltinnEventData)
        .filter(schema.AltinnEventData.id == db_id)
        .first()
    )
    return event_data


def _get_value_if_updated(
    old: Optional[datetime], new: Optional[datetime]
) -> Union[datetime, None]:
    if not new:
        return old
    if not old:
        return new
    return max([old, new])
