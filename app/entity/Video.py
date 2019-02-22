from app import db
from app.entity.Entity import Entity


class Video(Entity, db.Model):
    __tablename__ = "videos"

    VIDEO_PER_PAGE = 2

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(190), nullable=False)
    slug = db.Column(db.String(190), nullable=False)
    video = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    description = db.Column(db.Text)

    user = db.relationship('User', back_populates="videos")
    category = db.relationship('Category', back_populates="videos")

    def __init__(self, title, slug):
        Entity.__init__(self)
        self.title = title
        self.slug = slug
