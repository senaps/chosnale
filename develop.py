from Chosnale.application import create_app
from Chosnale.config import TEST_DB_URI

app = create_app(db_uri=TEST_DB_URI)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)