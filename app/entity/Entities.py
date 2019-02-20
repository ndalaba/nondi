
from app import db
from app.entity.Entity import Entity


class Work(Entity, db.Model):

    __tablename__ = "works"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(190), nullable=False)
    category = db.Column(db.String(190), nullable=False)
    techno = db.Column(db.String(190), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.Text)
    url = db.Column(db.String(190))
    image = db.Column(db.String(190), default='upload/noimage.png')

    user = db.relationship('User', back_populates="works")

    def __init__(self,title,user_id):
        Entity.__init__(self)
        self.title=title
        self.user_id=user_id


class Message(Entity, db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True)
    email_from = db.Column(db.String(150), nullable=False)
    email_to = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(190), nullable=False)
    message = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(190), nullable=False)
    phone = db.Column(db.String(190))
    read = db.Column(db.Boolean, default=False)
    folder = db.Column(db.String(50)) # INBOX, SENT, DRAFT, STRASH
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='emails')

    def __init__(self, user_id):
        Entity.__init__(self)
        self.user_id = user_id
