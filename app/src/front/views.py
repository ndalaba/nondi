from flask import render_template, url_for, jsonify, redirect, request
from flask_mail import Message as Msg

from app import mail
from app.src.entity.Article import Article, Category
from app.src.entity.Message import Message
from app.src.entity.User import User
from app.src.entity.Video import Video
from app.src.repository.Repository import Repository
from . import front
from .form import EmailForm

populars = Article.query.filter_by(published=True).order_by(Article.vue.desc()).paginate(1, 3, False)


@front.route('/')
def index():
    videos = Video.query.filter_by(published=True).order_by(Video.created_at.desc()).paginate(1, 6, False)
    divers = Article.query.filter_by(published=True, category_id=8).order_by(Article.created_at.desc()).paginate(1, 3, False)
    blogs = Article.query.filter_by(published=True, category_id=7, top=False).order_by(Article.created_at.desc()).paginate(1, 4, False)
    blog = Article.query.filter_by(published=True, category_id=7, top=True).order_by(Article.created_at.desc()).paginate(1, 1, False)
    articles = Article.query.filter_by(published=True, category_id=6, top=False).order_by(Article.created_at.desc()).paginate(1, 4, False)
    article = Article.query.filter_by(published=True, category_id=6, top=True).order_by(Article.created_at.desc()).paginate(1, 1, False)
    return render_template('front/home.html', videos=videos.items, blog=blog.items, blogs=blogs.items, articles=articles.items, article=article.items, populars=populars.items, divers=divers.items)


@front.route('/<cat_slug>')
def articles(cat_slug):
    page = request.args.get('page', 1, type=int)
    category = Category.query.filter_by(slug=cat_slug).first()
    if category is not None:
        articles = Article.query.filter_by(published=True,category_id=category.id).order_by(Article.created_at.desc()).paginate(page, Article.POSTS_PER_PAGE, False)
        next_url = url_for('front.articles', page=articles.next_num, cat_slug=cat_slug) if articles.has_next else None
        prev_url = url_for('front.articles', page=articles.prev_num, cat_slug=cat_slug) if articles.has_prev else None
        return render_template('front/articles.html', article=article, populars=populars.items, articles=articles.items, next_url=next_url, prev_url=prev_url, category=category)
    else:
        return redirect(url_for('front.article', category=cat_slug, slug=''))


@front.route('/<category>/<slug>')
def article(category, slug):
    article = Article.query.filter_by(slug=slug).first()
    if article is not None:
        article.vue = article.vue + 1
        Repository.save(article)
        articles = Article.query.filter(Article.published == True, Article.category_id == article.category_id, Article.id != article.id).order_by(Article.created_at.desc()).paginate(1, 3, False)
    else:
        articles = Article.query.filter(Article.published == True).order_by(Article.created_at.desc()).paginate(1, 10, False)
    return render_template('front/article.html', article=article, populars=populars.items, articles=articles.items)


@front.route('/contact', methods=['POST'])
def contact():
    form = EmailForm()
    if request.method == 'POST':
        if form.is_submitted():
            user = User.query.filter_by(uid=form.user.data).first()
            if user is None:
                return jsonify(type="error", text="Erreur formulaire.")
            email = Message(user_id=user.id)
            email.email_from = form.email.data
            email.folder = "INBOX"
            email.email_to = user.email
            email.subject = form.subject.data
            email.message = form.message.data
            email.name = form.name.data
            Repository.save(email)
            
            msg = Msg(email.subject, sender=(email.name,email.email_from), recipients=[user.email])
            msg.body = email.message
            mail.send(msg)

            return jsonify(type="success", text="Votre message a été envoyé.")
        return jsonify(type="error", text="Erreur formulaire.")
    return redirect(url_for('front.index'))
