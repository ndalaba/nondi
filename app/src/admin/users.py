from flask import render_template, redirect, request, flash, url_for
from flask_login import login_required
from slugify import slugify

from app.src.entity.User import User
from app.src.repository.Repository import Repository
from app.src.utils.auth import is_admin
from app.src.utils.upload import uploadImage
from . import admin
from .forms import UserForm


@admin.route('/users')
@is_admin
@login_required
def users():
    form = UserForm()
    page = request.args.get('page', 1, type=int)
    show_all = request.args.get('show_all', 0, type=int)
    if show_all:
        users = User.query.order_by(User.created_at.desc()).paginate(page, 10, False)
    else:
        users = User.query.filter_by(activated=False).order_by(User.created_at.desc()).paginate(page, 10, False)
    next_url = url_for('admin.articles', page=users.next_num, show_all=show_all) if users.has_next else None
    prev_url = url_for('admin.articles', page=users.prev_num, show_all=show_all) if users.has_prev else None
    return render_template('admin/users/users.html', form=form, users=users.items, url=url_for('admin.add_user'), prev_url=prev_url, next_url=next_url, show_all=show_all)


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
