from flask import Flask

from backend.models import Base, engine
from backend.views.authentication import authentication

app = Flask(__name__)
Base.metadata.create_all(engine)

app.register_blueprint(authentication, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)