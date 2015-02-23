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
import flask

try:
    import local_config
except ImportError as e:
    flask.logger.debug(e)
    raise e

# Miguel Grinberg's post 3 - flask-WTF
WTF_CSRF_ENABLED = True
SECRET_KEY = local_config.SECRET_KEY

# Miguel Grinberg's post 4 - databases
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# Using flask-migrate
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

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
