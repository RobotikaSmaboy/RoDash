from flask import jsonify
from flask import request
from werkzeug.security import check_password_hash

from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt

from roboys_dash.tables import AdminMember

from functools import wraps

def extractHTTPBasicAuth():
    pass

def jwt_or_auth_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            auth = request.authorization
            if auth.type == "basic":
                username, password = auth.parameters.values()

                admin = AdminMember.query.filter_by(username=username).first()
                if not admin:
                    return {"message": "User not found!"}, 400
                if not check_password_hash(admin.password, password):
                    return {"message": "Wrong password!"}, 400

            else:
                verify_jwt_in_request()

            return fn(*args, **kwargs)

        return decorator

    return wrapper
