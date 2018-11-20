import os
import datetime
from urllib.parse import quote

__all__ = ['db_uri', 'test_db_uri']


# we will read the database_uri elements from os environment_variables and
# initiate a db_uri. this is being used to connect and add the data to the db.
# quote() is used to escape special charachters form `username` and `password`
username = quote(os.environ.get('username', 'root'), safe='')
password = quote(os.environ.get('password', ''), safe='')
database = os.environ.get('database', 'localhost')
db_name = os.environ.get('db_name', 'chosnale')

db_uri = f"mysql+pymysql://{username}:{password}@{database}/{db_name}"

#  test db_uri
test_db_uri = "sqlite:////tmp/chosnale_test.db"
