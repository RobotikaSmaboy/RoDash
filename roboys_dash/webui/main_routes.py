from flask import Blueprint
from flask import make_response
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash

from roboys_dash.webui.utils import jwt_cookie_required
from roboys_dash.webui.utils import reqApiWithJwt

main = Blueprint("main", __name__)

@main.route("/")
@jwt_cookie_required
def home():
    apiReq = reqApiWithJwt("/overview", "GET", request=request).json()

    return render_template("home.html", data=apiReq)

@main.route("/member")
@jwt_cookie_required
def member():
    apiReq = reqApiWithJwt("/members", "GET", request=request).json()

    return render_template("daftar_member.html", data=apiReq)

@main.route("/member", methods=["POST"])
@jwt_cookie_required
def member_add():
    nama = request.form.get("addMemberName")
    nis = request.form.get("addMemberNIS")
    kelas = request.form.get("addMemberKelas")

    apiReq = reqApiWithJwt("/members", "POST", request=request, json={
        "name": nama,
        "nis": nis,
        "kelas": kelas
    }).json()

    return redirect(url_for("main.member"))

@main.route("/member/edit", methods=["POST"])
@jwt_cookie_required
def member_edit():
    nis = request.form.get("editMemberNIS")
    name = request.form.get("editMemberName")
    kelas = request.form.get("editMemberKelas")
    cardUid = request.form.get("editMemberUID")

    apiReq = reqApiWithJwt("/members", "PATCH", request=request, json={
        "nis": nis,
        "name": name,
        "kelas": kelas,
        "card_uid": cardUid
    }).json()

    return redirect(url_for("main.member"))

@main.route("/member/hapus", methods=["POST"])
@jwt_cookie_required
def member_delete():
    nis = request.form.get("deleteMemberNIS")

    apiReq = reqApiWithJwt("/members", "DELETE", request=request, json={
        "nis": nis
    }).json()

    return redirect(url_for("main.member"))

@main.route("/absen")
@jwt_cookie_required
def absen():
    apiReq = reqApiWithJwt("/absen", "GET", request=request).json()

    return render_template("absensi.html", data=apiReq)

@main.route("/absen", methods=["POST"])
@jwt_cookie_required
def absen_add():
    cardUid = request.form.get("addAbsenUID")
    tanggal = request.form.get("addAbsenTanggal")

    apiReq = reqApiWithJwt("/absen", "POST", request=request, json={
        "card_uid": cardUid,
        "tanggal": tanggal
    }).json()

    return redirect(url_for("main.absen"))

@main.route("/absen/hapus", methods=["POST"])
@jwt_cookie_required
def absen_delete():
    nis = request.form.get("deleteAbsenNIS")
    tanggal = request.form.get("deleteAbsenTanggal")

    apiReq = reqApiWithJwt("/absen", "DELETE", request=request, json={
        "nis": nis,
        "tanggal": tanggal
    }).json()

    return redirect(url_for("main.absen"))
