from models.user import db
from models.user import User

class BaseService:
    @staticmethod
    def create(instance):
        db.session.add(instance)
        db.session.commit()
        return instance

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
    
    def get_by_id(self, id):
        return self.model.query.get(id)
    
    def get_all(self):
        return self.model.query.all()