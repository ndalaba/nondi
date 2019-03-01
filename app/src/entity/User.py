# User entity

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from app.src.entity.Entity import Entity


class User(Entity, UserMixin, db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    location = db.Column(db.String(150))
    email = db.Column(db.String(60), unique=True, index=True)
    phone = db.Column(db.String(20), unique=True)
    role = db.Column(db.String(60), default="edition")
    password_hash = db.Column(db.String(130))
    photo = db.Column(db.String(130), unique=True)
    facebook = db.Column(db.String(190))
    activated = db.Column(db.Boolean, default=False)

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

    @property
    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return "User: {}".format(self.name)

    def __init__(self, name, email):
        Entity.__init__(self)
        self.email = email
        self.name = name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
