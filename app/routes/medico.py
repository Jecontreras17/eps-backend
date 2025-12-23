from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.utils.permissions import role_required

medico_bp = Blueprint("medico", __name__, url_prefix="/medico")

@medico_bp.route("/panel")
@jwt_required()
@role_required("medico")
def panel_medico():
    return jsonify({"msg": "Panel médico"})
