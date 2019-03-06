
from app import db
from app.src.entity.Entity import Entity
from app.src.utils.str_helper import strip_tags


class Category(Entity, db.Model):
    __tablename__ = "categories"

    CAT_PER_PAGE = 5

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

    POSTS_PER_PAGE = 14

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(190), nullable=False)
    slug = db.Column(db.String(190), nullable=False)
    top = db.Column(db.Boolean, default=0)
    content = db.Column(db.Text)
    content_extrait = db.column(db.Text)
    image = db.Column(db.String(190), default='upload/noimage.png')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    vue = db.Column(db.Integer, default=0)

    user = db.relationship('User', back_populates="articles")
    category = db.relationship('Category', back_populates="articles")

    def __init__(self, title,slug, user_id, category_id):
        Entity.__init__(self)
        self.title = title
        self.slug = slug
        self.user_id = user_id
        self.category_id = category_id
        self.image = 'noimage.png'

    def get_extrait(self, _len=100):
        return strip_tags(self.content[0:_len])

    def is_author(self, user):
        return self.user_id == user.id
