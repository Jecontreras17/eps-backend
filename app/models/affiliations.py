from flask import Blueprint, request, jsonify
from app.models.affiliation_request import AffiliationRequest
from app.utils.extensions import db

affiliation_bp = Blueprint("affiliations", __name__)

@affiliation_bp.route("/request", methods=["POST"])
def request_affiliation():
    data = request.get_json()

    req = AffiliationRequest(
        email=data["email"],
        full_name=data["full_name"],
        document_type=data["document_type"],
        document_number=data["document_number"],
        phone=data.get("phone"),
        birth_date=data.get("birth_date")
    )

    db.session.add(req)
    db.session.commit()

    return jsonify({"msg": "Solicitud enviada correctamente"}), 201
