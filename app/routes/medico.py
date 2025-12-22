from flask import Blueprint, jsonify
from app.utils.permissions import has_role

medico_bp = Blueprint("medico", __name__, url_prefix="/medico")

@medico_bp.route("/panel")
@has_role("medico")
def panel_medico():
    return jsonify({"msg": "Panel médico"})
