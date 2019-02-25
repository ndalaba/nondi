from app import db


class Repository:

    @staticmethod
    def query(entity):
        return db.session.query(entity)

    @staticmethod
    def save(entity):
        db.session.add(entity)
        db.session.commit()
    
    @staticmethod
    def delete(entity):
        db.session.delete(entity)
        db.session.commit()

    # Remove all articles with given uids
    @staticmethod
    def remove_all_by_uid(entity, uids):
        db.session.query(entity).filter(entity.uid.in_(uids)).delete(synchronize_session=False)
        db.session.commit()

    # Publish all articles with given uids
    @staticmethod
    def publish_all_by_uid(entity, uids):
        db.session.query(entity).filter(entity.uid.in_(uids)).update({entity.published: True}, synchronize_session=False)
        db.session.commit()

    # Unpublish all articles with given uids
    @staticmethod
    def un_publish_all_by_uid(entity, uids):
        db.session.query(entity).filter(entity.uid.in_(uids)).update(dict(published=False), synchronize_session=False)
        db.session.commit()

    # Set top all articles with given uids
    @staticmethod
    def set_top(entity, uids):
        db.session.query(entity).filter(entity.uid.in_(uids)).update({entity.top: True}, synchronize_session=False)
        db.session.commit()

    # Set normal all articles with given uids
    @staticmethod
    def set_normal(entity, uids):
        db.session.query(entity).filter(entity.uid.in_(uids)).update({entity.top: False}, synchronize_session=False)
        db.session.commit()
