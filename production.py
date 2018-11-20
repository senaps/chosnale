from Chosnale.application import create_app
from Chosnale.config import db_uri

app = create_app(db_uri=db_uri)

if __name__ == '__main__':
    app.run()