from models.user import User
from Services.base_service import BaseService

class UserService:
    @staticmethod
    def create_user(username, email, password):
        new_user = User(username=username, email=email, password=password)
        return BaseService.create(new_user)

    @staticmethod
    def get_user_by_id(user_id):
        return BaseService.get_by_id(User, user_id)

    @staticmethod
    def get_all_users():
        return BaseService.get_all(User)
