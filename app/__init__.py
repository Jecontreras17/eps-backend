from flask import Flask
from flask_jwt_extended import verify_jwt_in_request
from app.utils.extensions import db, jwt
from app.utils.config import Config
from app.utils.activity import update_last_activity

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # Blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.medico import medico_bp
    from app.routes.paciente import paciente_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp)
    app.register_blueprint(medico_bp)
    app.register_blueprint(paciente_bp)

    #  Control GLOBAL de inactividad
    @app.before_request
    def check_user_activity():
        try:
            verify_jwt_in_request(optional=True)
            update_last_activity()
        except Exception:
            return {"msg": "Sesión expirada por inactividad"}, 401

    return app
