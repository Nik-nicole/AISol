from models.user import User
from app import bcrypt, Config
from Services.base_service import BaseService

class UserService(BaseService):
    def __init__(self):
        super().__init__(User)
    
    def create_user(self, user):
        if not user.username or not user.email or not user.password_hash:
            raise ValueError("All fields are required")
        if self.model.query.filter_by(email=user.email).first():
            raise ValueError("Email is already registered")
        if len(user.password_hash) < Config.PASSWORD_MIN_LENGTH:
            raise ValueError(f"Password must be at least {Config.PASSWORD_MIN_LENGTH} characters long")
        user.password_hash = bcrypt.generate_password_hash(user.password_hash).decode('utf-8', 'ignore')
        return self.save(user)

    def authenticate_user(self, email, password):
        if not email or not password:
            raise ValueError("Email and password are required")
        user = self.model.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user
        return None