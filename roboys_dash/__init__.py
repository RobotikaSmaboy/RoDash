from flask import Flask

from flask_jwt_extended import JWTManager

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
appConfig = config["App"]
dbConfig = config["Database"]

# RoBoys API URL
API_URL = appConfig["API_URL"]

# JWT init
jwt = JWTManager()

# SQLAlchemy init
db = SQLAlchemy()

# Flask-Migrate init
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = appConfig["SECRET_KEY"]
    # app.config["PROPAGATE_EXCEPTIONS"] = True

    # JWT init
    app.config["JWT_SECRET_KEY"] = appConfig["SECRET_KEY"]
    jwt.init_app(app)

    # SQLAlchemy init
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        f"mysql://{dbConfig['USER']}:{dbConfig['PASS']}@{dbConfig['HOST']}:{dbConfig['PORT']}/{dbConfig['DB_NAME']}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Flask-Migrate init
    from roboys_dash.tables import AdminMember
    from roboys_dash.tables import Member
    migrate.init_app(app, db)

    # API: Home
    from roboys_dash.api.main_routes import home_bp
    app.register_blueprint(home_bp, url_prefix="/api")

    # API: Auth
    from roboys_dash.api.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api")

    # API: Overview
    from roboys_dash.api.overview_routes import overview_bp
    app.register_blueprint(overview_bp, url_prefix="/api")

    # API: Member
    from roboys_dash.api.members_routes import members_bp
    app.register_blueprint(members_bp, url_prefix="/api")

    # API: Absen
    from roboys_dash.api.absen_routes import absen_bp
    app.register_blueprint(absen_bp, url_prefix="/api")


    # Main routes
    from roboys_dash.webui.main_routes import main
    app.register_blueprint(main)

    # Auth routes
    from roboys_dash.webui.auth_routes import auth
    app.register_blueprint(auth)

    return app
