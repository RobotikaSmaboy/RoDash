# from flask import Flask

# from flask_sqlalchemy import SQLAlchemy

# from flask_jwt_extended import JWTManager

# from flask_migrate import Migrate

# from configparser import ConfigParser
# import json

# config = ConfigParser()
# config.read("config.ini")
# dbConfig = config["Database"]
# appConfig = config["App"]

# # JWT init
# jwt = JWTManager()

# # SQLAlchemy init
# db = SQLAlchemy()

# # Flask-Migrate init
# migrate = Migrate()


# def create_app():
#     app = Flask(__name__)
#     app.secret_key = appConfig["SECRET_KEY"]
#     app.config["PROPAGATE_EXCEPTIONS"] = True

#     # JWT init
#     app.config["JWT_SECRET_KEY"] = appConfig["SECRET_KEY"]
#     jwt.init_app(app)

#     # SQLAlchemy init
#     app.config["SQLALCHEMY_DATABASE_URI"] = \
#         f"mysql://{dbConfig['USER']}:{dbConfig['PASS']}@{dbConfig['HOST']}:{dbConfig['PORT']}/{dbConfig['DB_NAME']}"
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.init_app(app)

#     from api.tables import AdminMember
#     from api.tables import Member
#     from api.tables import RoAbsen

#     # Flask-Migrate init
#     migrate.init_app(app, db)


#     # Main routes API
#     from api.main_routes import home_bp
#     app.register_blueprint(home_bp)

#     # Overview routes API
#     from api.overview_routes import overview_bp
#     app.register_blueprint(overview_bp)

#     # Auth routes API
#     from api.auth_routes import auth_bp
#     app.register_blueprint(auth_bp)

#     # Members routes API
#     from api.members_routes import members_bp
#     app.register_blueprint(members_bp)

#     # Absen routes API
#     from api.absen_routes import absen_bp
#     app.register_blueprint(absen_bp)

#     # RoAbsen routes API
#     from api.RoAbsen_routes import RoAbsen_bp
#     app.register_blueprint(RoAbsen_bp)

#     return app
