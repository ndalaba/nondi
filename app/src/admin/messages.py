from flask import redirect, render_template, flash,url_for, request
from . import admin
from flask_login import login_required, current_user
from app.src.entity.Message import Message
from sqlalchemy import text
from app.src.repository.Repository import Repository
from flask_mail import Message as Msg
from app import mail
from app.src.utils.auth import is_admin


@admin.route('/messages',methods=['GET','POST'])
@login_required
@is_admin
def messages():
    if request.method=='POST':
        if request.form.get('action')=="remove":
            uids = request.form.getlist('uid')
            Repository.remove_all_by_uid(Message,uids)
    emails = Message.query.filter_by(user_id=current_user.id, folder='INBOX').order_by(text('created_at DESC'))[:15]
    #emails = Message.query.filter_by(user_id=current_user.id,folder='INBOX').order_by(text('created_at DESC')).limit(15).all()
    return render_template('admin/messages/index.html', emails=emails)


@admin.route('/messages/envoyes')
@login_required
@is_admin
def send_messages():
    emails = Message.query.filter_by(user_id=current_user.id, folder='SEND').order_by(text('created_at DESC'))[:15]
    return render_template('admin/messages/index.html', emails=emails)


@admin.route('/messages/nouveau',methods=('GET','POST'))
@login_required
@is_admin
def compose():
    if request.method == 'POST':
        new_mail = Message(user_id=current_user.id)
        new_mail.email_from = current_user.email
        new_mail.folder = "SEND"
        new_mail.email_to = request.form['email_to']
        new_mail.subject = request.form['subject']
        new_mail.message = request.form['message']
        new_mail.name = current_user.name
        Repository.save(new_mail)

        msg = Msg(new_mail.subject, sender=(new_mail.name, new_mail.email_from), recipients=[new_mail.email_to])
        msg.body = new_mail.message
        mail.send(msg)

        flash('Message envoyé', 'success')
        return redirect(url_for('admin.send_messages'))
    email = Message(user_id=current_user.id)
    email.email_from=current_user.email
    email.name=current_user.name
    return render_template('admin/messages/compose.html', email=email)


@admin.route('/messages/detail/<uid>')
@login_required
@is_admin
def read(uid):
    email = Message.query.filter_by(user_id=current_user.id, uid=uid).one()
    email.read=True
    Repository.save(email)
    return render_template('admin/messages/detail.html', email=email)


@admin.route('/messages/repondre/<uid>', methods=('GET', 'POST'))
@login_required
@is_admin
def repondre(uid):
    email = Message.query.filter_by(user_id=current_user.id, uid=uid).one()
    new_mail = Message(user_id=current_user.id)
    new_mail.email_from = current_user.email
    new_mail.email_to=email.email_from
    new_mail.subject = "Re: %s" % email.subject
    return render_template('admin/messages/compose.html', email=new_mail)


@admin.route('/message/supprimer/<uid>')
@login_required
@is_admin
def delete_message(uid):
    email = Message.query.filter_by(user_id=current_user.id, uid=uid).one()
    Repository.delete(email)
    flash('Message supprimé','success')
    return redirect(url_for('admin.messages'))
