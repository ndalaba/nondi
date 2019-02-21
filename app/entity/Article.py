
from app import db
from app.entity.Entity import Entity


class Category(Entity, db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(190), nullable=False)
    slug = db.Column(db.String(190), nullable=False)
    description = db.Column(db.Text)
    articles = db.relationship('Article', back_populates="category")
    videos = db.relationship('Video', back_populates="category")

    def __init__(self, title, slug):
        Entity.__init__(self)
        self.title = title
        self.slug = slug
        self.published = True


class Article(Entity, db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(190), nullable=False)
    slug = db.Column(db.String(190), nullable=False)
    top = db.Column(db.Boolean, default=0)
    content = db.Column(db.Text)
    image = db.Column(db.String(190), default='upload/noimage.png')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    user = db.relationship('User', back_populates="articles")
    category = db.relationship('Category', back_populates="articles")

    def __init__(self, title,slug, user_id, category_id):
        Entity.__init__(self)
        self.title = title
        self.slug = slug
        self.user_id = user_id
        self.category_id = category_id
