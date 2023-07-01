from flask import Blueprint

from flask_restful import Api, Resource, reqparse

from flask_jwt_extended import jwt_required

from roboys_dash import db
from roboys_dash.tables import Member
from roboys_dash.api.utils import jwt_or_auth_required

import json

members_bp = Blueprint("api_members", __name__)
members_api = Api(members_bp)

class MembersAPI(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()
        super().__init__()

    @jwt_or_auth_required()
    def get(self):
        self.parser.add_argument("nis", type=int, help="NIS siswa", location=["args"], required=False)
        args = self.parser.parse_args()

        member_query = Member.query
        if args.get("nis"):
            member = member_query.filter_by(nis=args.get("nis")).first()
            return member.serialize
        else:
            member = member_query.all()
            return [m.serialize for m in member]

    @jwt_or_auth_required()
    def post(self):
        self.parser.add_argument("name", type=str, help="Nama Member", required=True)
        self.parser.add_argument("nis", type=int, help="NIS siswa", required=True)
        self.parser.add_argument("kelas", type=str, help="Kelas Member", required=True)
        args = self.parser.parse_args()

        member = Member(
            name=args["name"],
            nis=args["nis"],
            kelas=args["kelas"]
        )
        db.session.add(member)
        db.session.commit()

        return member.serialize
    
    @jwt_or_auth_required()
    def patch(self):
        self.parser.add_argument("nis", type=int, help="NIS siswa", required=True)
        self.parser.add_argument("name", type=str, help="Nama Member", required=True)
        self.parser.add_argument("kelas", type=str, help="Kelas Member", required=True)
        self.parser.add_argument("card_uid", type=str, help="UID kartu Member", required=True)
        args = self.parser.parse_args()

        member = Member.query.filter_by(nis=args["nis"]).first()
        member.name = args["name"]
        member.kelas = args["kelas"]
        member.cardUid = args["card_uid"]
        db.session.add(member)
        db.session.commit()

        return member.serialize

    @jwt_or_auth_required()
    def delete(self):
        self.parser.add_argument("nis", type=int, help="NIS siswa", required=True)
        args = self.parser.parse_args()

        member = Member.query.filter_by(nis=args["nis"]).first()

        db.session.delete(member)
        db.session.commit()

        return member.serialize

class MembersUIDAPI(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()

        super().__init__()

    @jwt_required()
    def post(self):
        self.parser.add_argument("nis", type=int, help="NIS siswa", required=True)
        self.parser.add_argument("uid", type=str, help="UID kartu", required=True)
        args = self.parser.parse_args()

        member = Member.query.filter_by(nis=args["nis"]).first()

        uid = json.loads(member.cardUid)
        if args["uid"] in uid:
            return {"message": "UID already registered!"}, 400
        uid.append(args["uid"])
        member.cardUid = json.dumps(uid)
        db.session.commit()

        return member.serialize

    @jwt_required()
    def delete(self):
        self.parser.add_argument("nis", type=int, help="NIS siswa", required=True)
        self.parser.add_argument("uid", type=str, help="UID kartu", required=True)
        args = self.parser.parse_args()

        member = Member.query.filter_by(nis=args["nis"]).first()

        uid = json.loads(member.cardUid)
        if args["uid"] in uid:
            uid.remove(args["uid"])

        member.cardUid = json.dumps(uid)
        db.session.commit()

        return member.serialize

members_api.add_resource(MembersAPI, "/members")
members_api.add_resource(MembersUIDAPI, "/members/uid")
