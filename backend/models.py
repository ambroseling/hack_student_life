from flask_sqlalchemy import SQLAlchemy
from . import db


class Events(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    source_url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.ARRAY(db.String(255)), nullable=True) # seems like these have to be nullable else error upon create

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