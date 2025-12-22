from flask import Blueprint, jsonify
from app.utils.permissions import has_role

paciente_bp = Blueprint("paciente", __name__, url_prefix="/paciente")

@paciente_bp.route("/perfil")
@has_role("paciente")
def perfil():
    return jsonify({"msg": "Perfil del paciente"})
