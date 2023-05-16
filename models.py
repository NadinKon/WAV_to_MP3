from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(36), nullable=False)


class Audio(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    data = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


