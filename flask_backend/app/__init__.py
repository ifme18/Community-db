from flask import Flask
from .config import Config
from .models import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # register blueprints / routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
