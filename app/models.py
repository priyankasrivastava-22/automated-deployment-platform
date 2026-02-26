from .database import db
from datetime import datetime


class Environment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    status = db.Column(db.String(50))


class Build(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Deployment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String(50))
    version = db.Column(db.String(50))
    status = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class SystemMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpu = db.Column(db.Float)
    memory = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)