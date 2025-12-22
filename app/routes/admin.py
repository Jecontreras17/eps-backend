from flask import Blueprint, jsonify
from app.utils.permissions import has_role

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@has_role("admin")
def dashboard():
    return jsonify({"msg": "Panel de administrador"})
