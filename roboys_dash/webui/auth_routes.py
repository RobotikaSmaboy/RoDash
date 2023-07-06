from flask import Blueprint
from flask import render_template
from flask import make_response
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

import requests

from roboys_dash import API_URL

import json

auth = Blueprint("auth", __name__, template_folder="templates")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        next = request.form.get("next")

        loginReq = requests.post(API_URL + "/login", json={
            "username": username,
            "password": password
        }).json()

        if loginReq.get("message"):
            # Login failure handling
            flash(f"Error: {loginReq.get('message')}")
            return redirect(url_for("auth.login"))

        if next:
            homeResp = make_response(redirect(next))
        else:
            homeResp = make_response(redirect(url_for("main.home")))
        homeResp.set_cookie("access_token", loginReq["access_token"])

        return homeResp

    return render_template("login.html")

@auth.route("/logout")
def logout():
    loginResp = make_response(redirect(url_for("auth.login")))
    # if request.cookies.get("access_token"):
    #     loginResp.delete_cookie("access_token")
    loginResp.delete_cookie("access_token")

    return loginResp
