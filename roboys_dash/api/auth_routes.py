from flask import Blueprint

from flask_restful import Api, Resource, reqparse

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from datetime import datetime
from datetime import timedelta
from pytz import timezone

from roboys_dash import db
from roboys_dash.tables import AdminMember

auth_bp = Blueprint("api_auth", __name__)
auth_api = Api(auth_bp)

class LoginAPI(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username", type=str, help="Username", required=True)
        self.parser.add_argument("password", type=str, help="Password", required=True)

        super().__init__()
    def post(self):
        parser = self.parser.parse_args()

        member = AdminMember.query.filter_by(username=parser["username"]).first()
        if not member:
            return {"message": "Username not found!"}, 401

        if not check_password_hash(member.password, parser["password"]):
            return {"message": "Wrong Password!"}, 401

        # Generate JWT
        # JWT Expire: 60 minutes
        jktTimezone = timezone("Asia/Jakarta")
        currentDate = datetime.now(jktTimezone)

        accessTokenDelta = timedelta(minutes=60)
        accessTokenExpire = datetime.timestamp(currentDate + accessTokenDelta)
        accessToken = create_access_token(identity=parser["username"], expires_delta=accessTokenDelta)

        refreshTokenDelta = timedelta(days=2)
        refreshTokenExpire = datetime.timestamp(currentDate + refreshTokenDelta)
        refreshToken = create_refresh_token(identity=parser["username"], expires_delta=refreshTokenDelta)

        return {
            "user_info": member.serialize,
            "access_token": accessToken,
            "access_token_expire": accessTokenExpire,
            "refresh_token": refreshToken,
            "refresh_token_expire": refreshTokenExpire
        }

class RegisterAPI(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name", type=str, help="Nama user", required=True)
        self.parser.add_argument("username", type=str, help="Username", required=True)
        self.parser.add_argument("password", type=str, help="Password", required=True)

        super().__init__()
    def post(self):
        parser = self.parser.parse_args()

        member = AdminMember(
            name=parser["name"],
            username=parser["username"],
            password=generate_password_hash(parser["password"])
        )
        db.session.add(member)
        db.session.commit()

        return member.serialize

class RefreshAPI(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()
        super().__init__()

    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()

        jktTimezone = timezone("Asia/Jakarta")
        currentDate = datetime.now(jktTimezone)

        accessTokenDelta = timedelta(minutes=60)
        accessTokenExpire = datetime.timestamp(currentDate + accessTokenDelta)
        accessToken = create_access_token(identity=identity, expires_delta=accessTokenDelta, fresh=False)

        return {
            "access_token": accessToken,
            "access_token_expire": accessTokenExpire,
        }

class AdminsAPI(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()
        super().__init__()

    @jwt_required()
    def get(self):
        self.parser.add_argument("username", type=str, help="Username", location=["args"], required=False)
        args = self.parser.parse_args()

        member_query = AdminMember.query
        if args.get("username"):
            member = member_query.filter_by(username=args.get("username")).first()
            return member.serialize
        else:
            member = member_query.all()
            return [m.serialize for m in member]

auth_api.add_resource(LoginAPI, "/login")
auth_api.add_resource(RegisterAPI, "/register")
auth_api.add_resource(RefreshAPI, "/refresh")
auth_api.add_resource(AdminsAPI, "/admins")
