from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.utils.permissions import role_required

paciente_bp = Blueprint("paciente", __name__, url_prefix="/paciente")

@paciente_bp.route("/perfil")
@jwt_required()
@role_required("paciente","admin","superadmin","medico")
def perfil():
    return jsonify({"msg": "Perfil del paciente"})
