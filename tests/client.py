import os
import tempfile

import pytest

from Chosnale.application import create_app


@pytest.fixture
def client():
    db, app = create_app(configs={'db_uri': tempfile.mkstemp(), 'testing':True})
    flaskr.app.config['TESTING'] = True
    client = flaskr.app.test_client()

    with flaskr.app.app_context():
        flaskr.init_db()

    yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])