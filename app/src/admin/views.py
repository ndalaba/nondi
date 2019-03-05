from flask import render_template
from flask_login import login_required, current_user

from app.src.entity.Article import Article, Category
from app.src.entity.Page import Page
from app.src.entity.User import User
from app.src.entity.Video import Video
from . import admin
from .forms import Article as ArticleForm


@admin.route('/home')
@admin.route('/')
@login_required
def home():
    form = ArticleForm()
    categories = Category.query.all()
    if current_user.is_admin:
        articles_published = Article.query.filter_by(published=True).count()
        videos_published = Video.query.filter_by(published=True).count()
        users_activated = User.query.filter_by(activated=True).count()
        page_activated = Page.query.filter_by(published=True).count()
        users = User.query.filter_by(activated=False).order_by(User.created_at.desc()).all()
        return render_template('admin/home.html', articles_published=articles_published, users=users, videos_published=videos_published, users_activated=users_activated, page_activated=page_activated, form=form, categories=categories)
    else:
        articles_published = Article.query.filter_by(published=True, user_id=current_user.id).count()
        videos_published = Video.query.filter_by(published=True, user_id=current_user.id).count()
        return render_template('admin/home.html', articles_published=articles_published, videos_published=videos_published, form=form, categories=categories)
