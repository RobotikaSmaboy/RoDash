from flask import Blueprint
from flask import Flask

from flask_restful import Api, Resource, reqparse

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from roboys_dash import db
from roboys_dash.tables import AdminMember

auth_bp = Blueprint("api_auth", __name__)
auth_api = Api(auth_bp, errors=Flask.errorhandler)

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
        # JWT Expire: Never
        accessToken = create_access_token(identity=parser["username"], expires_delta=False)

        return {
            "user_info": member.serialize,
            "access_token": accessToken,
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
auth_api.add_resource(AdminsAPI, "/admins")
