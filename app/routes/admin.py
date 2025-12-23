from datetime import datetime
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from app.models.affiliation_request import AffiliationRequest
from app.models.role import Role
from app.models.user import User
from app.utils.permissions import role_required 
from app.utils.extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@jwt_required()
@role_required("admin","superadmin")
def dashboard():
    return jsonify({"msg": "Panel de administrador"})

def is_admin():
    claims = get_jwt()
    return "admin" in claims["roles"] or "super_admin" in claims["roles"]

@admin_bp.route("/affiliations/pending", methods=["GET"])
@jwt_required()
def list_pending_requests():
    if not is_admin():
        return {"msg": "Acceso denegado"}, 403

    requests = AffiliationRequest.query.filter_by(status="pending").all()

    return jsonify([
        {
            "id": r.id,
            "email": r.email,
            "type": r.request_type,
            "data": r.data,
            "created_at": r.created_at
        }
        for r in requests
    ])

@admin_bp.route("/affiliations/<int:req_id>/approve", methods=["POST"])
@jwt_required()
def approve_affiliation(req_id):
    if not is_admin():
        return {"msg": "Acceso denegado"}, 403

    affiliation = AffiliationRequest.query.get_or_404(req_id)

    if affiliation.status != "pending":
        return {"msg": "Solicitud ya procesada"}, 400

    user = User.query.filter_by(email=affiliation.email).first()

    if not user:
        return {"msg": "Usuario no existe"}, 404

    # Rol paciente siempre
    patient_role = Role.query.filter_by(name="paciente").first()
    if patient_role not in user.roles:
        user.roles.append(patient_role)

    # Si es médico
    if affiliation.request_type == "medico":
        medico_role = Role.query.filter_by(name="medico").first()
        if medico_role not in user.roles:
            user.roles.append(medico_role)

    affiliation.status = "approved"
    affiliation.reviewed_by = get_jwt_identity()
    affiliation.reviewed_at = datetime.utcnow()

    db.session.commit()

    return {"msg": "Solicitud aprobada correctamente"}

@admin_bp.route("/affiliations/<int:req_id>/reject", methods=["POST"])
@jwt_required()
def reject_affiliation(req_id):
    if not is_admin():
        return {"msg": "Acceso denegado"}, 403

    affiliation = AffiliationRequest.query.get_or_404(req_id)

    if affiliation.status != "pending":
        return {"msg": "Solicitud ya procesada"}, 400

    affiliation.status = "rejected"
    affiliation.reviewed_by = get_jwt_identity()
    affiliation.reviewed_at = datetime.utcnow()

    db.session.commit()

    return {"msg": "Solicitud rechazada"}
