from flask_sqlalchemy import SQLAlchemy

__all__ = [
    'db',
]

db = SQLAlchemy()

class Shadow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Shadow %r>' % self.email

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msg_filename = db.Column(db.String(120), unique=True, nullable=False)
    msg_date = db.Column(db.DateTime, unique=False, nullable=False)
    msg_subject = db.Column(db.Text, unique=False, nullable=False)
    msg_from_name = db.Column(db.String(64), unique=False, nullable=False)
    msg_from_addr = db.Column(db.String(64), unique=False, nullable=False)
    msg_to_name = db.Column(db.String(64), unique=False, nullable=False)
    msg_to_addr = db.Column(db.String(64), unique=False, nullable=False)
    msg_text = db.Column(db.Text, nullable=False)
    msg_html = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Message %r>' % self.username
