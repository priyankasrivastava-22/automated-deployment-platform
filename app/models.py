from datetime import datetime
from .database import db


# class Build(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     status = db.Column(db.String(50), nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Deployment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)