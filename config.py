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
