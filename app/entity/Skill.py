
from app import db
from app.entity.Entity import Entity


class Skill(Entity, db.Model):

    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(190), nullable=False)
    level = db.Column(db.String(190), nullable=False)
    experience = db.Column(db.Integer)
    percent = db.Column(db.Integer)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates="skills")
