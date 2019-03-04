from flask import Blueprint

front = Blueprint('front', __name__)

from . import views
from app.src.entity.Article import Article
from app.src.entity.Page import Page


@front.context_processor
def inject_value():
    populars = Article.query.filter_by(published=True).order_by(Article.vue.desc()).paginate(1, 3, False)
    pages = Page.query.filter_by(published=True).paginate(1, 3, False)
    return dict(populars=populars.items, pages=pages.items)
