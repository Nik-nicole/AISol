from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models.user import User
from services.base_service import BaseService

bcrypt = Bcrypt()

class UserService(BaseService):
    model = User  # Define el modelo

    @classmethod
    def register(cls, username, email, password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        return cls.create(username=username, email=email, password=hashed_password)

    @classmethod
    def login(cls, email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return create_access_token(identity=user.id)
        return None
