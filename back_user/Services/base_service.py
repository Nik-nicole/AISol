from models.user import db

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
