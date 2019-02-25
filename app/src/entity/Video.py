from app import db
from app.src.entity.Entity import Entity


class Video(Entity, db.Model):
    __tablename__ = "videos"

    VIDEO_PER_PAGE = 10

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(190), nullable=False)
    slug = db.Column(db.String(190), nullable=False)
    video = db.Column(db.String(190), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    description = db.Column(db.Text)
    vue = db.Column(db.Integer, default=0)

    user = db.relationship('User', back_populates="videos")
    category = db.relationship('Category', back_populates="videos")

    def __init__(self, title, slug, user_id, category_id):
        Entity.__init__(self)
        self.title = title
        self.slug = slug
        self.user_id = user_id
        self.category_id = category_id