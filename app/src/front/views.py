from flask import render_template, url_for, jsonify, redirect, request
from app.src.entity.User import User
from app.src.repository.Repository import Repository
from . import front
from .form import EmailForm
from flask_mail import Message as Msg
from app import mail
from app.src.entity.Message import Message


@front.route('/')
def index():

    user = User.query.filter_by(uid='a6c5a240').first()

    form = EmailForm()
    return render_template('front/base.html', user=user)


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
