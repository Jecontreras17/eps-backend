from flask import Flask, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_limiter import Limiter
from app.utils.extensions import db, jwt
from app.utils.config import Config
from app.utils.activity import update_last_activity
from flask_cors import CORS as Cors
from app.utils.extensions import limiter


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Cors(app, 
         origins=["http://127.0.0.1:5500", "http://localhost:5500","http://localhost:3000"],
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
         )
    
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)  #  Inicializar rate limiter

    # Blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.medico import medico_bp
    from app.routes.paciente import paciente_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(medico_bp, url_prefix="/medico")
    app.register_blueprint(paciente_bp, url_prefix="/paciente")

    #  Control GLOBAL de inactividad
    @app.before_request
    def track_activity():
        public_endpoints = [
            '/auth/login', 
            '/auth/register', 
            '/auth/refresh'
        ]
        
        if request.path in public_endpoints:
            return
        
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                update_last_activity()
        except Exception:
            pass

    return app
