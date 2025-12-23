from app.utils.extensions import db
from datetime import datetime

class AffiliationRequest(db.Model):
    __tablename__ = "affiliation_requests"

    id = db.Column(db.Integer, primary_key=True)

    # Puede existir o no el usuario aún
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    email = db.Column(db.String(120), nullable=False)

    request_type = db.Column(
        db.String(20), 
        nullable=False
    )  
    # paciente | medico

    status = db.Column(
        db.String(20), 
        default="pending"
    )
    # pending | approved | rejected

    data = db.Column(db.JSON, nullable=False)
    # datos personales, EPS, especialidad, etc.

    reviewed_by = db.Column(
        db.Integer, 
        db.ForeignKey("users.id"), 
        nullable=True
    )

    reviewed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AffiliationRequest {self.email} ({self.request_type})>"
