from app import create_app
from app.utils.extensions import db
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

app = create_app()

with app.app_context():

    db.create_all()
    print(" Tablas creadas correctamente")
    
    # Verificar que se crearon
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f" Tablas en la base de datos: {tables}")