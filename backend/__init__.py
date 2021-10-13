from flask import Flask

def create_app():
    from .models import Base, engine
    from .views.authentication import authentication

    app = Flask(__name__)
    Base.metadata.create_all(engine)

    app.register_blueprint(authentication, url_prefix='/auth')
    return app
