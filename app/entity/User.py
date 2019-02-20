# User entity

from app.entity.Entity import Entity
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(Entity, UserMixin, db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    location = db.Column(db.String(150))
    email = db.Column(db.String(60), unique=True, index=True)
    phone = db.Column(db.String(20), unique=True)
    role = db.Column(db.String(60))
    password_hash = db.Column(db.String(130))
    photo = db.Column(db.String(130), unique=True)
    facebook = db.Column(db.String(150))

    articles = db.relationship('Article', back_populates="user")
    messages = db.relationship('Message', back_populates="user")
    videos = db.relationship('Video', back_populates="user")

    @property
    def password(self):
        raise AttributeError('Peut pas modifier directement le mot de passe')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "User: {}".format(self.name)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
