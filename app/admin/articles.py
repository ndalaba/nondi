from flask import render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from slugify import slugify

from app.entity.Article import Article
from app.entity.Article import Category
from app.repository.Repository import Repository
from app.utils.upload import uploadImage
from . import admin
from .forms import Article as ArticleForm


@admin.route('/articles')
@login_required
def articles():
    categories = Category.query.all()
    page = request.args.get('page', 1, type=int)
    if current_user.is_admin:
        articles = Article.query.order_by(Article.created_at.desc()).paginate(page, Article.POSTS_PER_PAGE, False)
    else:
        articles = Article.query.filter_by(user_id=current_user.id).order_by(Article.created_at.desc()).paginate(page, Article.POSTS_PER_PAGE, False)
    next_url = url_for('admin.articles', page=articles.next_num) if articles.has_next else None
    prev_url = url_for('admin.articles', page=articles.prev_num) if articles.has_prev else None
    return render_template('admin/articles/articles.html', articles=articles.items, categories=categories, next_url=next_url, prev_url=prev_url)


@admin.route('/articles/add', methods=['POST','GET'])
@login_required
def add_article():
    form = ArticleForm()
    categories = Category.query.all()
    if request.method == 'POST':
        if form.validate_on_submit:
            article = Article(title=form.title.data, slug=slugify(form.title.data), user_id=current_user.id, category_id=form.category.data)
            if form.image.data:
                image = uploadImage(form.image.data, 'upload/articles/')
                article.image = image
            article.content = form.content.data
            article.published = form.published.data
            article.top = form.top.data
            Repository.save(article)
            flash("Article ajouté avec succès", 'success')
            return redirect(url_for('admin.articles'))
        else:
            flash('Formulaire incorrect', 'error')
    else:
        return render_template('admin/articles/form.html',form=form, categories=categories, url=url_for('admin.add_article'))


@admin.route('/articles/edit/<uid>', methods=['GET', 'POST'])
@login_required
def edit_article(uid):
    article = Article.query.filter_by(uid=uid).first()
    form = ArticleForm(obj=article)
    categories = Category.query.all()
    if request.method == 'POST':
        if form.validate_on_submit:
            if form.image.data and form.image.data != article.image:
                image = uploadImage(form.image.data, 'upload/articles/')
                article.image = image
            article.title = form.title.data
            article.top = form.top.data
            slug_title = slugify(form.title.data)
            article.slug = slug_title
            article.content = form.content.data
            article.category_id = form.category.data
            article.published = form.published.data
            Repository.save(article)
            flash("Article modifié avec succès", 'success')
            return redirect(url_for('admin.articles'))
        else:
            flash('Formulaire incorrect', 'error')
    return render_template('admin/articles/form.html', form=form,  categories=categories, url=url_for('admin.edit_article', uid=uid), article=article)


@admin.route('/articles/delete/<uid>')
@login_required
def delete_article(uid):
    article = Article.query.filter_by(uid=uid).first()
    Repository.delete(article)
    flash("Article supprimé avec succès", 'success')
    return redirect(url_for('admin.articles'))
