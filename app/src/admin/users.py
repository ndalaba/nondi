from flask import render_template, redirect, request, flash, url_for
from flask_login import login_required
from slugify import slugify

from app.src.entity.User import User
from app.src.repository.Repository import Repository
from app.src.utils.auth import is_admin
from app.src.utils.upload import uploadImage
from . import admin
from .forms import UserForm
from flask_mail import Message as Msg
from app import mail


@admin.route('/users')
@is_admin
@login_required
def users():
    page = request.args.get('page', 1, type=int)
    action = request.args.get('doaction') if request.args is not None else ""
    if action == "Appliquer":
        todo = float(request.args.get('todo'))
        uids = request.args.getlist('uid')
        if todo == -1:
            Repository.remove_all_by_uid(User, uids)
        elif todo == 1:
            Repository.activate_all_by_uid(User, uids)
            users= User.query.filter(User.uid.in_(uids)).all()
            with mail.connect() as conn:
                for user in users:
                    message = "Bonjour %s, \n Votre compte Nondi a été activé. \n Vous êtes libre d'ajouter autant d'articles, de vidéos que vous voulez sur la plateforme" % user.name
                    subject = "Compte Nondi activé"
                    msg = Msg(recipients=[user.email], body=message, subject=subject, sender=("Nondi Guinée", "contact@nondi.org"))
                    conn.send(msg)
        elif todo == 0:
            Repository.deactivate_all_by_uid(User, uids)
        return redirect(url_for('admin.users'))
    elif action == "Filtrer":
        email = request.args.get('email')
        active = request.args.get('active')
        query = Repository.query(User)
        query = query.filter(User.email.like('%' + email + '%')) if email is not None and email != "" else query
        query = query.filter(User.activated == int(active)) if active is not None and active.isnumeric() else query
        users = query.order_by(User.created_at.desc()).paginate(page, 13, False)
        
        next_url = url_for('admin.users', page=users.next_num, todo=9999, email=email, active=active, doaction='Filtrer') if users.has_next else None
        prev_url = url_for('admin.users', page=users.prev_num, todo=9999, email=email, active=active, doaction='Filtrer') if users.has_prev else None

    else:
        users = User.query.order_by(User.created_at.desc()).paginate(page,13, False)
        
        next_url = url_for('admin.users', page=users.next_num) if users.has_next else None
        prev_url = url_for('admin.users', page=users.prev_num) if users.has_prev else None
    return render_template('admin/users/users.html',  users=users.items, url=url_for('admin.add_user'), prev_url=prev_url, next_url=next_url)


@admin.route('/users/add', methods=['POST'])
@is_admin
@login_required
def add_user():
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            user = User(email=form.email.data, name=slugify(form.name.data))
            if form.photo.data:
                photo = uploadImage(form.photo.data, 'upload/users/')
                user.photo = photo
            user.phone = form.phone.data
            user.role = form.role.data
            user.password = request.form.get('password')
            user.facebook = form.facebook.data
            user.location = form.location.data
            user.activated = form.activated.data
            Repository.save(user)
            flash("Membre ajouté avec succès", 'success')
            return redirect(url_for('admin.users'))
        else:
            flash('Formulaire incorrect', 'error')
    else:
        return render_template('admin/users/form.html', form=form, url=url_for('admin.add_user'))


@admin.route('/users/edit/<uid>', methods=['GET', 'POST'])
@is_admin
@login_required
def edit_user(uid):
    user = User.query.filter_by(uid=uid).first()
    form = UserForm(obj=user)

    if request.method == 'POST':
        if form.validate_on_submit:
            if form.photo.data and form.photo.data != user.photo:
                photo = uploadImage(form.photo.data, 'upload/users/')
                user.photo = photo
            user.phone = form.phone.data
            user.name = form.name.data
            user.email = form.email.data
            user.role = request.form.get('role')
            if request.form.get('password'):
                user.password = request.form.get('password')
            user.facebook = form.facebook.data
            user.location = form.location.data
            user.activated = form.activated.data
            Repository.save(user)
            flash("Membre modifié avec succès", 'success')
            return redirect(url_for('admin.users'))
        else:
            flash('Formulaire incorrect', 'error')
    return render_template('admin/users/form.html', form=form, url=url_for('admin.edit_user', uid=uid), user=user)


@admin.route('/users/delete/<uid>')
@is_admin
@login_required
def delete_user(uid):
    user = User.query.filter_by(uid=uid).first()
    Repository.delete(user)
    flash("Membre supprimé avec succès", 'success')
    return redirect(url_for('admin.users'))
