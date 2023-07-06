from flask import request as flaskReq
from flask import flash
from flask import redirect
from flask import url_for

import requests

from functools import wraps

from roboys_dash import API_URL


def reqApiWithJwt(URL: str, method: str, json: dict = {}, request: flaskReq = None, accessToken: str = None):
    if not accessToken:
        accessToken = request.cookies.get("access_token")
    headers = {
        "Authorization": "Bearer " + accessToken
    }
    apiReq = requests.request(method=method, url=API_URL + URL, headers=headers, json=json)
    return apiReq

def jwt_cookie_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        next_url = flaskReq.path
        login_url = url_for("auth.login") + "?next=" + next_url

        # Check if JWT exists
        if not all([x in flaskReq.cookies.keys() for x in ["access_token"]]):
            # No JWT: asks user to login
            flash("Harap login terlebih dahulu!")
            return redirect(login_url)

        return f(*args, **kwargs)
    return decorated_function
