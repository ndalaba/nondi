from flask import render_template, url_for, jsonify, redirect, request
from flask_mail import Message as Msg

from app import mail
from app.src.entity.Article import Article, Category
from app.src.entity.Message import Message
from app.src.entity.Page import Page
from app.src.entity.Person import Person
from app.src.entity.User import User
from app.src.entity.Video import Video
from app.src.repository.Repository import Repository
from . import front
from .form import EmailForm, UserForm
from sqlalchemy import text


@front.route('/')
def index():
    videos = Video.query.filter_by(published=True).order_by(Video.created_at.desc()).paginate(1, 6, False)
    divers = Article.query.filter_by(published=True, category_id=8).order_by(Article.created_at.desc()).paginate(1, 3, False)
    blogs = Article.query.filter_by(published=True, category_id=7, top=False).order_by(Article.created_at.desc()).paginate(1, 4, False)
    blog = Article.query.filter_by(published=True, category_id=7, top=True).order_by(Article.created_at.desc()).paginate(1, 1, False)
    articles = Article.query.filter_by(published=True, category_id=6, top=False).order_by(Article.created_at.desc()).paginate(1, 4, False)
    article = Article.query.filter_by(published=True, category_id=6, top=True).order_by(Article.created_at.desc()).paginate(2, 1, False)
    top = Article.query.filter_by(published=True, category_id=6, top=True).order_by(Article.created_at.desc()).paginate(1, 1, False)
    return render_template('front/home.html', videos=videos.items, blog=blog.items, blogs=blogs.items, articles=articles.items, article=article.items, divers=divers.items, top=top.items[0])


@front.route('/rechercher')
def rechercher():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', "", type=str)
    articles = Article.query.filter(text("articles.published=1 AND LOWER(articles.title) LIKE LOWER('%"+q+"%')")).order_by(Article.created_at.desc()).paginate(page, Article.POSTS_PER_PAGE, False)
    next_url = url_for('front.rechercher', page=articles.next_num, q=q) if articles.has_next else None
    prev_url = url_for('front.rechercher', page=articles.prev_num, q=q) if articles.has_prev else None
    return render_template('front/articles.html', articles=articles.items, next_url=next_url, prev_url=prev_url, q=q)


@front.route('/videos/<slug>')
def videos(slug):
    page = request.args.get('page', 1, type=int)
    video = Video.query.filter_by(published=True, slug=slug).first()
    if video is not None:
        videos = Video.query.filter(Video.published == True, Video.id != video.id).order_by(Video.created_at.desc()).paginate(page, 6, False)
        next_url = url_for('front.videos', page=videos.next_num, slug=slug) if videos.has_next else None
        prev_url = url_for('front.videos', page=videos.prev_num, slug=slug) if videos.has_prev else None
        return render_template('front/videos.html', video=video, videos=videos.items, next_url=next_url, prev_url=prev_url, page=page)
    else:
        return redirect(url_for('front.article', category=slug, slug=slug))


@front.route('/nondi/<slug>')
def page(slug):
    page = Page.query.filter_by(slug=slug).first()
    if page is not None:
        persons = Person.query.filter_by(published=True).all()
        return render_template('front/page.html', page=page, persons=persons)
    else:
        return redirect(url_for('front.article', category=slug, slug=slug))


@front.route('/collaborateurs/<slug>')
def persons(slug):
    person = Person.query.filter_by(published=True, slug=slug).first()
    if person is not None:
        persons = Person.query.filter(Person.published == True, Person.id != person.id).all()
        return render_template('front/person.html', person=person, persons=persons)
    else:
        return redirect(url_for('front.article', category=slug, slug=slug))


@front.route('/<cat_slug>')
def articles(cat_slug):
    page = request.args.get('page', 1, type=int)
    category = Category.query.filter_by(slug=cat_slug).first()
    if category is not None:
        articles = Article.query.filter_by(published=True,category_id=category.id).order_by(Article.created_at.desc()).paginate(page, Article.POSTS_PER_PAGE, False)
        next_url = url_for('front.articles', page=articles.next_num, cat_slug=cat_slug) if articles.has_next else None
        prev_url = url_for('front.articles', page=articles.prev_num, cat_slug=cat_slug) if articles.has_prev else None
        return render_template('front/articles.html', article=article, articles=articles.items, next_url=next_url, prev_url=prev_url, category=category)
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
    return render_template('front/article.html', article=article, articles=articles.items)


@front.route('/contact', methods=['POST', 'GET'])
def contact():
    form = EmailForm()
    if request.method == 'POST':
        if form.is_submitted():
            email = Message(user_id=2)
            email.email_from = form.email.data
            email.folder = "INBOX"
            email.email_to = "contact@nondi.org"
            email.subject = form.subject.data
            email.message = form.message.data
            email.name = form.name.data
            Repository.save(email)
            
            msg = Msg(email.subject, sender=(email.name,email.email_from), recipients=["contact@nondi.org"])
            msg.body = email.message
            mail.send(msg)

            return jsonify(type="success", text="Votre message a été envoyé.")
        return jsonify(type="error", text="Erreur formulaire.")
    else:
        return render_template('front/contact.html')


@front.route('/s-enregistrer', methods=['POST', 'GET'])
def register():
    form = UserForm()
    if request.method == 'POST':
        if form.is_submitted():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None:
                return jsonify(type="error", text="Adresse email déjà utilisée, Veillez vous connecter")
            user = User.query.filter_by(phone=form.phone.data).first()
            if user is not None:
                return jsonify(type="error", text="Numéro de téléphone déjà utilisée, Veillez vous connecter")
            user = User(name=form.name.data, email=form.email.data)
            user.facebook = form.facebook.data
            user.phone = form.phone.data
            user.password = form.password.data
            user.photo = 'no-image.png'
            user.role = "editeur"
            user.activated = False
            Repository.save(user)
            return jsonify(type="success", text="Votre compte est en attente de validation")
        return jsonify(type="error", text="Erreur formulaire.")
    else:
        return render_template('front/register.html')
