from flask import render_template, url_for, jsonify, redirect, request
from app.src.entity.User import User
from app.src.repository.Repository import Repository
from . import front
from .form import EmailForm
from flask_mail import Message as Msg
from app import mail
from app.src.entity.Message import Message
from app.src.entity.Video import  Video


@front.route('/')
def index():
    videos = Video.query.order_by(Video.created_at.desc()).paginate(1, 6, False)
    return render_template('front/home.html',videos=videos.items)


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
