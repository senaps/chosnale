import os
import pytest

from Chosnale.application import create_app
from Chosnale.extensions import db


@pytest.fixture
def client():
    uri = "/tmp/tests_chosnale.db"
    db_uri = "sqlite:///" + uri
    app = create_app(db_uri=db_uri)
    client = app.test_client()
    yield client
    os.remove(uri)