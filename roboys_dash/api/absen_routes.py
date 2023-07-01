from flask import Blueprint

from flask_restful import Api, Resource, reqparse

from flask_jwt_extended import jwt_required

from roboys_dash import db
from roboys_dash.tables import Member
from roboys_dash.tables import Absen
from roboys_dash.api.utils import jwt_or_auth_required

from datetime import datetime
from pytz import timezone

import json

absen_bp = Blueprint("api_absen", __name__)
absen_api = Api(absen_bp)

class AbsenAPI(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()

        super().__init__()

    @jwt_required()
    def get(self):
        self.parser.add_argument("nis", type=int, location="args", required=False)
        parser = self.parser.parse_args()

        absen_query = Absen.query
        if parser.get("nis"):
            absen = absen_query.filter_by(nis=parser.get("nis")).all()
            return [a.serialize for a in absen]
        else:
            absen = absen_query.all()
            return [a.serialize for a in absen]

    @jwt_or_auth_required()
    def post(self):
        self.parser.add_argument("card_uid", type=str, help="Member UID", required=True)
        self.parser.add_argument("tanggal", type=str, help="Tanggal absen", required=False)
        parser = self.parser.parse_args()

        if parser["tanggal"]:
            parser["tanggal"] = datetime.strptime(parser["tanggal"], "%Y-%m-%d")
        else:
            jktTimezone = timezone("Asia/Jakarta")
            parser["tanggal"] = datetime.now(jktTimezone)

        member = Member.query.filter_by(cardUid=parser["card_uid"]).first()
        if not member:
            return {"message": "Member not found!"}, 400

        absen = Absen.query.filter(Absen.nis == member.nis, Absen.tanggal == datetime.strftime(parser["tanggal"], "%Y-%m-%d")).first()
        if absen:
            return {"message": "Sudah absen"}, 400

        absen = Absen(
            nis=member.nis,
            tanggal=parser["tanggal"],
            cardUid=parser["card_uid"]
        )
        db.session.add(absen)
        db.session.commit()

        return absen.serialize
    
    def delete(self):
        self.parser.add_argument("nis", type=int, help="NIS member", required=True)
        self.parser.add_argument("tanggal", type=str, help="Tanggal absen", required=True)
        parser = self.parser.parse_args()

        # parser["tanggal"] = datetime.strptime(parser["tanggal"], "%Y-%m-%d")
        absen = Absen.query.filter(Absen.nis == parser["nis"], Absen.tanggal == parser["tanggal"]).first()
        if not absen:
            return {"message": "Absen not found!"}, 400
        
        db.session.delete(absen)
        db.session.commit()

        return absen.serialize

absen_api.add_resource(AbsenAPI, "/absen")
