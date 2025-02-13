from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from Routes.user_routes import user_bp
from models import db  # 👈 Importa db desde models/__init__.py
from models.user import User  # 👈 Importa el modelo antes de inicializar la app

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar la base de datos
db.init_app(app)

# Inicializar Flask-Migrate
migrate = Migrate(app, db)  # ✅ Ahora detectará los modelos correctamente

# Inicializar JWT
jwt = JWTManager(app)

# Registrar Blueprints
app.register_blueprint(user_bp, url_prefix='/api/users')

if __name__ == '__main__':
    app.run(debug=True)
