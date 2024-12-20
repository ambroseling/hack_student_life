from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from sqlalchemy.types import TypeDecorator
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TSVECTOR
from . import db


class TSVector(TypeDecorator):
    impl = TSVECTOR
    cache_ok = True # for performance and to avoid a warning


class Events(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    source_url = db.Column(db.String(255))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.ARRAY(db.String(255)), nullable=True) # seems like these have to be nullable else error upon create
    ts_vector = db.Column(TSVector(),db.Computed("to_tsvector('english', title || ' ' || description)", persisted=True))   
    __table_args__ = (Index('ix_events_ts_vector',ts_vector, postgresql_using='gin'),)
    
    def serialize(self):
        return {
            "id": self.id,
            "source_url": self.source_url,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "location": self.location,
            "tags": self.tags,
        }