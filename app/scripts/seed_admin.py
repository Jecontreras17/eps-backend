from app import create_app
from app.utils.extensions import db
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("🔧 Creando roles y permisos...")
    
    # Crear roles
    roles_data = ['superadmin', 'admin', 'medico', 'paciente']
    roles = {}
    
    for role_name in roles_data:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)
            print(f"  Rol '{role_name}' creado")
        roles[role_name] = role
    
    # Crear permisos
    permissions_data = [
        'users:read', 'users:write', 'users:delete',
        'appointments:read', 'appointments:write', 'appointments:delete',
        'reports:read', 'reports:write',
        'settings:read', 'settings:write'
    ]
    
    for perm_name in permissions_data:
        permission = Permission.query.filter_by(name=perm_name).first()
        if not permission:
            permission = Permission(name=perm_name)
            db.session.add(permission)
            print(f"  Permiso '{perm_name}' creado")
    
    db.session.commit()
    
    # Asignar TODOS los permisos al superadmin
    superadmin_role = roles['superadmin']
    all_permissions = Permission.query.all()
    superadmin_role.permissions = all_permissions
    
    print("\n Creando usuario superadmin...")
    
    # Crear superadmin
    superadmin = User.query.filter_by(email='superadmin@eps.com').first()
    
    if not superadmin:
        superadmin = User(
            email='superadmin@eps.com',
            password=generate_password_hash('SuperAdmin123!'),
            is_active=True
        )
        db.session.add(superadmin)
        db.session.commit()
        
        # Asignar rol
        superadmin.roles.append(superadmin_role)
        db.session.commit()
        
        print("    Superadmin creado exitosamente")
        print("\n" + "="*50)
        print("    Email: superadmin@eps.com")
        print("    Contraseña: SuperAdmin123!")
        print("="*50 + "\n")
    else:
        print("     Superadmin ya existe")
        print(f"    Email: {superadmin.email}")
    
    print("Proceso completado")