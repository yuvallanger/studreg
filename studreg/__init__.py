"""
Studreg, Hafakulta's student union membership management system.

Copyright (C) 2014,2015 Yuval Langer.

This file is part of Studreg.

Studreg is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Studreg is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Studreg.  If not, see <http://www.gnu.org/licenses/>.
"""


import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID

from config import basedir

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app import views, models, forms
