from app import db

class Repository:

    def save(self,entity):
        db.session.add(entity)
        db.session.commit()
    
    def delete(self,entity):
        db.session.delete(entity)
        db.session.commit()

repository= Repository()