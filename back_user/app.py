from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from db import db
from Routes.user_routes import user_bp

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar la base de datos
db.init_app(app)

# Inicializar JWT
jwt = JWTManager(app)

# Registrar Blueprints
app.register_blueprint(user_bp, url_prefix='/api/users')

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
