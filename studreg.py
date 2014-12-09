#!/usr/bin/env python

from __future__ import (
    absolute_import, division, print_function, unicode_literals,
)
from builtins import *

import json
from functools import wraps, update_wrapper

# import logging
# from logging import FileHandler

from flask import Flask, request, g
import flask.ext.sqlalchemy

import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy import Column, Float, Integer, String, Table, Text, text
from sqlalchemy.ext.declarative import declarative_base


# our app configuration
import studreg_config

# http://stackoverflow.com/questions/14398329/can-sqlalchemy-automatically-create-relationships-from-a-database-schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = studreg_config.MYSQL_URI
db = flask.ext.sqlalchemy.SQLAlchemy(app)

class Ezor(db.Model):
    __tablename__ = 'ezor'

    id = Column(Integer, primary_key=True)
    ezor = Column(Integer, nullable=False)
    hug = Column(Integer, nullable=False)


class Studentreg(db.Model):
    __tablename__ = 'studentreg'

    id = Column(String(10), primary_key=True, unique=True)
    fname = Column(Text, nullable=False)
    lname = Column(Text, nullable=False)
    email = Column(Text)
    tel = Column(Float, index=True)
    campus = Column(Text)
    faculty = Column(Text)
    degree = Column(Text)
    year = Column(Text)
    major = Column(Text)
    minor = Column(Text)
    revaha = Column(Text)
    miluim = Column(Integer, nullable=False, server_default=text("'0'"))
    arab = Column(Integer, nullable=False, server_default=text("'0'"))
    matana = Column(Integer, nullable=False, server_default=text("'0'"))
    dorms = Column(Integer, nullable=False, server_default=text("'0'"))
    extra1 = Column(Integer, nullable=False, server_default=text("'0'"))
    extra2 = Column(Integer, nullable=False, server_default=text("'0'"))
    extra3 = Column(Integer, nullable=False, server_default=text("'0'"))
    extra4 = Column(Integer, nullable=False, server_default=text("'0'"))
    extra5 = Column(Integer, nullable=False, server_default=text("'0'"))
    extra6 = Column(Integer, nullable=False, server_default=text("'0'"))
    extra7 = Column(Integer, nullable=False, server_default=text("'0'"))
    extra8 = Column(Integer, nullable=False, server_default=text("'0'"))
    extra9 = Column(Integer, nullable=False, server_default=text("'0'"))
    extra10 = Column(Integer, nullable=False, server_default=text("'0'"))
    didRegister = Column(Integer, nullable=False)


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(16), unique=True)
    password = Column(String(50))
    is_active = Column(Integer, nullable=False)
    usertype = Column(String(11), nullable=False)
# http://arusahni.net/blog/2014/03/flask-nocache.html

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = (
            'no-store, no-cache, '
            'must-revalidate, post-check=0, '
            'pre-check=0, max-age=0'
        )
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(view, no_cache)


def find_membership(identity_numbers):
    s = sqlalchemy.sql.select([studentreg]).where(identi)
    result = conn.execute(s)


@app.route('/api/1/<func_name>', methods=['POST'])
#@nocache
def api_1(func_name):
    if func_name == 'find_membership':
        data = json.loads(request.post.identity_number)
        identity_number = data.keys()[0]
        if Studentreg.query.filter(id==data).first() is None:
            return
        member_dict = find_membership(request.post.identity_numbers)
        return json.dumps(member_dict)


@app.route('/')
#@nocache
def root():
    return ' '.join([request.path, request.method])

@app.route('/update/')
#@nocache
def update():
    return ' '.join([request.path, request.method])


def app_run():
    app.run(
        port=5001,
    )

def test_query():
    print(Studentreg.query.filter(Studentreg.id=='888411485').first().id)
    #db_session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(bind=db))
    #for item in db_session.query(models.Studentreg):
    #    print(item)


if __name__ == '__main__':
    test_query()
    #app_run()
