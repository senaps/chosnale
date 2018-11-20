import os
import datetime
from urllib.parse import quote

__all__ = ['TEST_DB_URI', 'PRODUCTION_DB_URI']


# we will read the database_uri elements from os environment_variables and
# initiate a db_uri. this is being used to connect and add the data to the db.
# quote() is used to escape special charachters form `username` and `password`
USERNAME = quote(os.environ.get('username', 'root'), safe='')
PASSWORD = quote(os.environ.get('password', ''), safe='')
DATABASE = os.environ.get('database', 'localhost')
DB_NAME = os.environ.get('db_name', 'chosnale')

PRODUCTION_DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{DATABASE}/{DB_NAME}"

#  test db_uri
TEST_DB_URI = "sqlite:////tmp/chosnale_test.db"
