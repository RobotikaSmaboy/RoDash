from flask import request as flaskReq
from flask import flash
from flask import redirect
from flask import url_for
from flask import make_response

from datetime import datetime
from pytz import timezone

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

        # Check if JWT is almost expire
        if not all([x in flaskReq.cookies.keys() for x in ["access_token", "access_token_expire"]]):
            # No JWT: asks user to login
            flash("Harap login terlebih dahulu!")
            return redirect(login_url)

        jktTimezone = timezone("Asia/Jakarta")
        currentDatestamp = datetime.timestamp(datetime.now(jktTimezone))

        if float(currentDatestamp) >= float(flaskReq.cookies.get("access_token_expire")):
            if float(currentDatestamp) >= float(flaskReq.cookies.get("refresh_token_expire")):
                flash("Sesi berakhir. Harap login kembali!")
                loginResp = make_response(redirect(login_url))
                loginResp.delete_cookie("access_token")
                loginResp.delete_cookie("access_token_expire")

                return loginResp
            else:
                # TODO: Access token expires but refresh token doesn't;
                # refresh access token and do nothing
                req = reqApiWithJwt(URL="/refresh", method="POST", accessToken=flaskReq.cookies.get("refresh_token")).json()
                resp = make_response(f(*args, **kwargs))
                # resp = redirect(f(*args, **kwargs))
                resp.set_cookie("access_token", req.get("access_token"))
                resp.set_cookie("access_token_expire", str(req.get("access_token_expire")))

                # return resp
                respNew = make_response(resp)
                return respNew

        return f(*args, **kwargs)
    return decorated_function
