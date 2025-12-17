from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt()
        print("Identity:", identity) 
        if identity.get("role") != "admin":
            return jsonify({"message": "Admin access required"}), 403

        return fn(*args, **kwargs)
    return wrapper
