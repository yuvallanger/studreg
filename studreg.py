#!/usr/bin/env python

from __future__ import (
    absolute_import, division, print_function, unicode_literals,
)
from builtins import *

from functools import wraps, update_wrapper

# import logging
# from logging import FileHandler

from flask import Flask, request, g


app = Flask(__name__)


def connect_db():
    return None

#@app.before_request
def before_request():
    g.db = connect_db()

#@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

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

@app.route('/')
@nocache
def root():
    return ' '.join([request.path, request.method])

@app.route('/update/')
@nocache
def update():
    return ' '.join([request.path, request.method])

if __name__ == '__main__':
    app.run(
        port=5001
    )
