from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from flask_migrate import Migrate


mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_name=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_name)
    db.init_app(app)
    login_manager.init_app(app)

    # if app.config['SSL_REDIRECT']:
    #     from flask_sslify import SSLify
    #     sslify = SSLify(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    return app
