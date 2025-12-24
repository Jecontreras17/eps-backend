import os
from app import create_app
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == "__main__":

      # Verificar que las claves se cargaron
    if not os.getenv('SECRET_KEY') or os.getenv('SECRET_KEY').startswith('dev-fallback'):
        print("⚠️ ADVERTENCIA: Usando clave de desarrollo por defecto")
        print("   Crea un archivo .env con SECRET_KEY y JWT_SECRET_KEY")
    
    app.run(host='127.0.0.1', port=5000, debug=True)