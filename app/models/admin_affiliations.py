from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.utils.permissions import has_role
from app.models.affiliation_request import AffiliationRequest
from app.models.user import User
from app.models.patient_profile import PatientProfile
from app.utils.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash

admin_aff_bp = Blueprint("admin_affiliations", __name__)

@admin_aff_bp.route("/approve/<int:request_id>", methods=["POST"])
@jwt_required()
@has_role("admin")
def approve_affiliation(request_id):
    req = AffiliationRequest.query.get_or_404(request_id)

    if req.status != "pending":
        return {"msg": "Solicitud ya procesada"}, 400

    user = User(
        email=req.email,
        password=generate_password_hash("temporal123"),
        is_active=True
    )

    db.session.add(user)
    db.session.flush()

    patient = PatientProfile(
        user_id=user.id,
        full_name=req.full_name,
        document_type=req.document_type,
        document_number=req.document_number,
        phone=req.phone,
        birth_date=req.birth_date
    )

    req.status = "approved"
    req.reviewed_at = datetime.utcnow()

    db.session.add(patient)
    db.session.commit()

    return {"msg": "Paciente creado correctamente"}
