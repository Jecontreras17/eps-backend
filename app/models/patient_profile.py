from app.utils.extensions import db

class PatientProfile(db.Model):
    __tablename__ = "patient_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    full_name = db.Column(db.String(150), nullable=False)
    document_type = db.Column(db.String(20), nullable=False)
    document_number = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    address = db.Column(db.String(200))

    user = db.relationship("User", backref="patient_profile")

    def __repr__(self):
        return f"<PatientProfile {self.full_name}>"
