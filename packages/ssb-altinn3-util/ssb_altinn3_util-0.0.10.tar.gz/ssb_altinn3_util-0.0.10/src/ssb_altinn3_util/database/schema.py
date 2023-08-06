from sqlalchemy import Integer, DateTime, String, ForeignKey, Column
from sqlalchemy.orm import relationship

from ssb_altinn3_util.database.altinn_mottak_db_adapter import AltinnMottakDbAdapter


class AltinnEvent(AltinnMottakDbAdapter.Base):
    __tablename__ = "altinn_event"

    db_id = Column("id", Integer, primary_key=True, index=True)
    id = Column("event_id", String, unique=True, index=True)
    time = Column(DateTime)
    source = Column(String)
    type = Column(String)
    subject = Column(String)
    alternativesubject = Column(String)
    data = Column(String)
    specversion = Column(String)
    datacontenttype = Column(String)

    process = relationship("AltinnEventProcess", uselist=False)
    event_data = relationship("AltinnEventData", uselist=False)


class AltinnEventProcess(AltinnMottakDbAdapter.Base):
    __tablename__ = "altinn_event_process"

    id = Column("id", Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("altinn_event.id"), unique=True, index=True)
    received_at = Column(DateTime)
    data_fetched_at = Column(DateTime)
    confirmed_altinn_at = Column(DateTime)
    confirmed_ssb_at = Column(DateTime)
    shared_at = Column(DateTime)
    deadlettered = Column(DateTime)


class AltinnEventData(AltinnMottakDbAdapter.Base):
    __tablename__ = "altinn_event_data"

    id = Column("id", Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("altinn_event.id"), unique=True, index=True)
    instance = Column(String)
    data_base_url = Column(String)
