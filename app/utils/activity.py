from datetime import datetime, timedelta
from flask_jwt_extended import get_jwt_identity
from flask import current_app
from app.models.user import User
from app.utils.extensions import db

def update_last_activity():
    user_id = get_jwt_identity()
    if not user_id:
        return

    user = User.query.get(user_id)
    if not user:
        return

    now = datetime.utcnow()
    limit = timedelta(
        minutes=current_app.config["INACTIVITY_LIMIT_MINUTES"]
    )

    if user.last_activity and now - user.last_activity > limit:
        raise Exception("SESSION_EXPIRED")

    user.last_activity = now
    db.session.commit()
