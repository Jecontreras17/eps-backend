import os
from app import create_app
from app.utils.extensions import db
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from werkzeug.security import generate_password_hash

app = create_app()

ROLES = ["super_admin", "admin", "medico", "paciente"]

PERMISSIONS = [
    "create_admin",
    "assign_roles",
    "approve_affiliation",
    "manage_users"
]

SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL")
SUPER_ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")

if not SUPER_ADMIN_EMAIL or not SUPER_ADMIN_PASSWORD:
    raise RuntimeError(" Faltan variables de entorno del super admin")


with app.app_context():

    print("▶ Creando permisos...")
    perms = {}
    for name in PERMISSIONS:
        perm = Permission.query.filter_by(name=name).first()
        if not perm:
            perm = Permission(name=name)
            db.session.add(perm)
        perms[name] = perm
    db.session.commit()

    print(" Creando roles...")
    roles = {}
    for name in ROLES:
        role = Role.query.filter_by(name=name).first()
        if not role:
            role = Role(name=name)
            db.session.add(role)
        roles[name] = role
    db.session.commit()

    print(" Asignando permisos al super_admin...")
    roles["super_admin"].permissions = list(perms.values())
    db.session.commit()

    print(" Creando super admin...")
    user = User.query.filter_by(email=SUPER_ADMIN_EMAIL).first()
    if not user:
        user = User(
            email=SUPER_ADMIN_EMAIL,
            password=generate_password_hash(SUPER_ADMIN_PASSWORD),
            is_active=True
        )
        user.roles.append(roles["super_admin"])
        db.session.add(user)
        db.session.commit()
        print(" Super admin creado")
    else:
        print(" Super admin ya existe")

    print(" Sistema inicializado")
