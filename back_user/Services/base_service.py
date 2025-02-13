from models.user import db
from models.user import User

class BaseService:
    @staticmethod
    def create(User):
        db.session.add(User)
        db.session.commit()
        return User

    @staticmethod
    def get_by_id(model, id):
        return model.query.get(id)

    @staticmethod
    def get_all(model):
        return model.query.all()

    @staticmethod
    def delete(instance):
        db.session.delete(instance)
        db.session.commit()
