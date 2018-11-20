from Chosnale.application import create_app
from Chosnale.config import PRODUCTION_DB_URI

app = create_app(db_uri=PRODUCTION_DB_URI)

if __name__ == '__main__':
    app.run()