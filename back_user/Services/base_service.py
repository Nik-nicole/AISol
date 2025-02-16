from app import db
class BaseService:
    def __init__(self, model):
        self.model = model
    
    def save(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity

    def delete(self, entity):
        db.session.delete(entity)
        db.session.commit()
    
    def get_by_id(self, id):
        return self.model.query.get(id)
    
    def get_all(self):
        return self.model.query.all()