import flask

try:
    import local_config
except ImportError as e:
    flask.logger.debug(e)

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
