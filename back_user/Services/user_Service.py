import os
from models.user import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from base_service.BaseService import create

# Define un "pepper" (clave secreta adicional para el hash)
PEPPER = os.getenv("SECRET_PEPPER", "clave-secreta-muy-fuerte")

class UserService:
    @staticmethod
    def create_user(username, email, password):
        # Generar un hash con scrypt + pepper
        salted_password = password + PEPPER
        hashed_password = generate_password_hash(salted_password)

        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()
        if not user:
            return None

        # Verificar la contraseña usando el pepper
        salted_password = password + PEPPER
        if check_password_hash(user.password, salted_password):
            access_token = create_access_token(identity=user.id)
            return access_token
        return None

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)
