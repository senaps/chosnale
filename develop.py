from Chosnale.application import create_app
from Chosnale.config import test_db_uri

app = create_app(configs={'db_uri': test_db_uri})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)