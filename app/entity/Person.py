from app import db
from app.entity.Entity import Entity


class Person(Entity, db.Model):
    __tablename__ = "persons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(190), nullable=False)
    slug = db.Column(db.String(190), nullable=False)
    function = db.Column(db.String(190))
    content = db.Column(db.Text)
    image = db.Column(db.String(190), default='upload/noimage.png')

    def __init__(self, name, slug):
        Entity.__init__(self)
        self.name = name
        self.slug = slug
