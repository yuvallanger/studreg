from app import db


class User(db.Model):
    idn = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {!r}>'.format(self.nickname)


class Student(db.Model):
    idn = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(140))
    last_name = db.Column(db.String(140))
    email = db.Column(db.String(140))
    id_card_number = db.Column(db.String(140), unique=True)
    events = db.relationship('Event', backref='students', lazy='dynamic')

    def __repr__(self):
        return '<Student {!r}>'.format(self.id_card_number)


class Event(db.Model):
    idn = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    name = db.Column(db.String(140))
    description = db.Column(db.String(512))
