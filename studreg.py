#!/usr/bin/env python

from __future__ import (
    absolute_import, division, print_function, unicode_literals,
)
from builtins import *

from functools import wraps


import flask
import flask.logging
from flask import Flask, request
from flask.ext import restful
import flask.ext.restful.reqparse
import flask.ext.sqlalchemy

# For the models
from sqlalchemy import Column, Float, Integer, String, Table, Text, text

#######################
#### Configuration ####
#######################

import local_config

MYSQL_URI = (
    'mysql+pymysql://'
    '{username}:{password}@'
    '{host}/{database}'
).format(
    username=local_config.mysql['username'],
    password=local_config.mysql['password'],
    host=local_config.mysql['host'],
    database=local_config.mysql['database'],
)

######################
#### Creating app ####
######################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_URI
db = flask.ext.sqlalchemy.SQLAlchemy(app)

api = restful.Api(app)

logger = flask.logging.create_logger(app)

########################
#### Authentication ####
########################

def check_auth(username, password):
    return username == 'admin' and password == 'password'


def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials',
        401,
        {
            'WWW-Authenticate': 'Basic realm="Login Required"',
        },
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

################
#### Models ####
################

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

##################
#### No cache ####
##################

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

#############
#### API ####
#############

parser = restful.reqparse.RequestParser()
parser.add_argument('identity_number', type=str, help='Student identity number')
parser.add_argument('email', type=str, help='Student e-mail address')

def find_membership_status(identity_number, email):
    logger.debug('arguments: {}'.format((identity_number, email)))

    some_res = Studentreg.query.first()
    logger.debug('some_res {}',format((some_res.id, some_res.email)))

    sql_query_result = Studentreg.query.get(identity_number)

    # Student record exists
    if sql_query_result is None:
        return 1

    # Student email is valid
    if sql_query_result.email.strip() != email.strip():
        return 2

    # Student doesn't belong to aguda
    if sql_query_result.revaha == u'0':
        return 3

    # Student belongs to aguda
    if sql_query_result.revaha == u'1':
        return 4

class MembershipStatus(restful.Resource):
    def post(self):
        args = parser.parse_args()
        membership_status = find_membership_status(
            identity_number=args['identity_number'].strip(),
            email=args['email'].strip(),
        )
        return dict(membership_status=membership_status)


api.add_resource(
    MembershipStatus,
    '/api/v1.0/membership_status/',
)

##############
#### Main ####
##############

if __name__ == '__main__':
    app.run(
        port=5001,
        debug=True,
    )
