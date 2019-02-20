
from app import db
from app.entity.Entity import Entity


class Work(Entity, db.Model):

    __tablename__ = "works"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(190), nullable=False)
    techno = db.Column(db.String(190), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.Text)

    user = db.relationship('User', back_populates="works")
