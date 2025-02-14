from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config

# Inicialización
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)  # Agregar esta línea

from Routes.user_routes import user_bp
app.register_blueprint(user_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)
