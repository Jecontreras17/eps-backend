from flask import Blueprint, request, jsonify
from app.models.user import User
from app.utils.extensions import db
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from datetime import datetime
from app.utils.extensions import limiter
from app.utils.validators import is_strong_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Datos incompletos"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Credenciales inválidas"}), 401

    if not user.is_active:
        return jsonify({"msg": "Usuario desactivado"}), 403

    roles = [role.name for role in user.roles]

    access = create_access_token(
        identity=user.id,
        additional_claims={"roles": roles}
    )

    refresh = create_refresh_token(identity=user.id)

    #  iniciar contador de inactividad
    user.last_activity = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "access_token": access,
        "refresh_token": refresh,
        "roles": roles
    })


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    roles = [role.name for role in user.roles]

    new_access = create_access_token(
        identity=user_id,
        additional_claims={"roles": roles}
    )

    return jsonify({"access_token": new_access})


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    password = data.get("password")
    
    #  Validar contraseña fuerte
    is_valid, message = is_strong_password(password)
    if not is_valid:
        return jsonify({"msg": message}), 400