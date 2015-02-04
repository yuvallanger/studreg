#!/usr/bin/env python

from __future__ import (
    absolute_import, division, print_function, unicode_literals,
)
from builtins import *

from functools import wraps

import flask
import flask.logging
from flask import Flask, request
import flask.ext.sqlalchemy
import flask.ext.restful
import flask.ext.restful.reqparse

# For the models
from sqlalchemy import Float, Text, text, String, Integer, Column

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

api = flask.ext.restful.Api(app)

logger = flask.logging.create_logger(app)

########################
#### Authentication ####
########################


def check_auth(username, password):
    logger.debug((username, password))
    authorized = local_config.api_user.get(username, None) == password
    return authorized


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return flask.Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'},
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        logger.debug(auth)
        if not auth or not check_auth(auth.username, auth.password):
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


class Revaha(object):
    DOES_NOT_BELONG = u'0'
    BELONGS = u'1'


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

#############
#### API ####
#############

parser = flask.ext.restful.reqparse.RequestParser()
parser.add_argument('email', type=str, help='Student e-mail address')


class AgudaMembershipTokens(object):
    MEMBER = u'member'
    NOT_MEMBER = u'not_member'


class StudentExistenceTokens(object):
    STUDENT_EXISTS = u'student_exists'
    STUDENT_MISSING = u'student_missing'


def get_membership_status(email):
    """
    :type email:  str
    :rtype : dict
    """
    logger.debug('arguments: {}'.format((email)))

    email = email.strip()

    sql_query_result = Studentreg.query.filter_by(email=email).first()

    # Student record does not exist
    if sql_query_result is None:
        return dict(
            student_existence=StudentExistenceTokens.STUDENT_MISSING,
        )

    # Student does not belong to the agudaorg.
    if sql_query_result.revaha == Revaha.DOES_NOT_BELONG:
        return dict(
            aguda_membership_status=AgudaMembershipTokens.NOT_MEMBER,
        )

    # Student belongs to agudaorg
    if sql_query_result.revaha == Revaha.BELONGS:
        return dict(
            aguda_membership_status=AgudaMembershipTokens.MEMBER,
        )


class MembershipStatus(flask.ext.restful.Resource):
    @requires_auth
    def post(self):
        email = request.form['email']
        return get_membership_status(
            email=email.strip(),
        )

    def get(self):
        email = request.args['email']

        return get_membership_status(
            email=email.strip(),
        )


api.add_resource(MembershipStatus, '/beta/membership_status')

##############
#### Main ####
##############

if __name__ == '__main__':
    app.run(
        port=local_config.port,
        debug=local_config.debug,
    )
