from app import db
from app.src.entity.Entity import Entity


class Message(Entity, db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    email_from = db.Column(db.String(150), nullable=False)
    email_to = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(190), nullable=False)
    message = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(190), nullable=False)
    phone = db.Column(db.String(190))
    read = db.Column(db.Boolean, default=False)
    folder = db.Column(db.String(50))  # INBOX, SENT, DRAFT, STRASH
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='messages')

    def __init__(self, user_id):
        Entity.__init__(self)
        self.user_id = user_id
