# Base Entity

from datetime import datetime
from sqlalchemy import Column, String, DateTime, event, Boolean
from app.utils.str_helper import generate_uuid

class Entity(object):

    uid = Column(String(30),index=True,unique=True,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    published = Column(Boolean, default=False)

    def __init__(self):
        self.uid=generate_uuid(5)
    
    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, 'before_update', cls._updated_at)
