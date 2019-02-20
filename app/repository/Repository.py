from app import db


class Repository:

    @staticmethod
    def save(entity):
        db.session.add(entity)
        db.session.commit()
    
    @staticmethod
    def delete(entity):
        db.session.delete(entity)
        db.session.commit()


# repository = Repository()
