from flask import Flask
from app.utils.extensions import db, jwt
from app.utils.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.medico import medico_bp
    from app.routes.paciente import paciente_bp
 
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp)
    app.register_blueprint(medico_bp)
    app.register_blueprint(paciente_bp)

    return app
