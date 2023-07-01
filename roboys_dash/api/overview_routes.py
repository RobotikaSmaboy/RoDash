from flask import Blueprint

from flask_restful import Api, Resource

from roboys_dash import db
from roboys_dash.tables import Member
from roboys_dash.tables import Absen
from roboys_dash.api.utils import jwt_or_auth_required

overview_bp = Blueprint("api_overview", __name__)
overview_api = Api(overview_bp)

class OverviewAPI(Resource):
    @jwt_or_auth_required()
    def get(self):
        memberTotal = Member.query.count()
        absenTotal = Absen.query.count()

        return {
            "member_total": memberTotal,
            "absen_total": absenTotal
        }

overview_api.add_resource(OverviewAPI, "/overview")
