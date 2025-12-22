from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt

def has_role(required_role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            roles = claims.get("roles", [])

            if required_role not in roles:
                return jsonify({
                    "msg": "No tienes permisos para acceder a este recurso"
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator

