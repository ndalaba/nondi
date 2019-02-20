
from app import db
from app.entity.Entity import Entity


class Education(Entity, db.Model):

    __tablename__ = "educations"

    id = db.Column(db.Integer, primary_key=True)
    formation = db.Column(db.String(190), nullable=False)
    location = db.Column(db.String(190), nullable=False)
    school = db.Column(db.String(190), nullable=False)
    begin = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.Text)

    user = db.relationship('User', back_populates="educations")
