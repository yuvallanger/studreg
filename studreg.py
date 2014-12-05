#!/usr/bin/env python

from flask import (
    Flask, request, session, g, redirect, url_for,
    abort, render_template, flash,
)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
