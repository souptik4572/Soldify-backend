from flask import Flask
from flask_cors import CORS


def create_app():
    from .models import Base, engine
    from .views.authentication import authentication
    from .views.product import product
    from .views.interested import interested
    from .views.sold import sold

    app = Flask(__name__)
    CORS(app)
    Base.metadata.create_all(engine)

    app.register_blueprint(authentication, url_prefix='/auth')
    app.register_blueprint(sold, url_prefix='/product/<int:product_id>/sold')
    app.register_blueprint(
        interested, url_prefix='/product/<int:product_id>/interested')
    app.register_blueprint(product, url_prefix='/product')
    return app
