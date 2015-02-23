from flask import (
    render_template, flash, redirect, session, url_for, request, g
)
from flask.ext.login import (
    login_user, logout_user, current_user, login_required
)

from .app import app, db, lm, oid
from .forms import LoginForm
from .models import User


@app.route('/')
@app.route('/index')
def index():
    user = dict(nickname='Miguel')
    posts = [
        dict(
            author=dict(nickname='John'),
            body='poop',
        ),
        dict(
            author=dict(nickname='Susan'),
            body='peep',
        ),
    ]
    return render_template(
        'index.html',
        # title='Home',
        user=user,
        posts=posts,
    )


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.valicate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
