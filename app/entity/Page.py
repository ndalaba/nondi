from app import db
from app.entity.Entity import Entity


class Page(Entity, db.Model):
    __tablename__ = "pages"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(190), nullable=False)
    slug = db.Column(db.String(190), nullable=False)
    content = db.Column(db.Text)
    image = db.Column(db.String(190), default='upload/noimage.png')

    def __init__(self, title, slug):
        Entity.__init__(self)
        self.title = title
        self.slug = slug
