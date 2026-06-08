from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(32), default='Analyst', nullable=False) # Admin, Investigator, Analyst

class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String(64), unique=True, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(32), default='Active', nullable=False) # Active, Suspended, Closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    evidence_items = db.relationship('Evidence', backref='associated_case', lazy=True)

class Evidence(db.Model):
    __tablename__ = 'evidence_log'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    filename = db.Column(db.String(256), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    file_type = db.Column(db.String(64), nullable=False) # Image, Video, Audio, Document
    md5_hash = db.Column(db.String(32), nullable=False)
    sha256_hash = db.Column(db.String(64), nullable=False)
    authenticity_score = db.Column(db.Float, nullable=False)
    ai_probability = db.Column(db.Float, nullable=False)
    forensic_metadata = db.Column(db.JSON, nullable=True)
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)
    logs = db.relationship('ChainOfCustody', backref='evidence', lazy=True)

class ChainOfCustody(db.Model):
    __tablename__ = 'chain_of_custody'
    id = db.Column(db.Integer, primary_key=True)
    evidence_id = db.Column(db.Integer, db.ForeignKey('evidence_log.id'), nullable=False)
    action = db.Column(db.String(256), nullable=False) # Uploaded, Analyzed, Transferred, Exported
    operator_username = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)