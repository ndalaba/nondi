from flask_login import login_required, current_user
from flask import render_template, redirect, request, flash, url_for
from . import admin
from app.repository.Repository import repository
from app.entity.Entities import Hobby
from .forms import Hobby as HobbyForm


@admin.route('/hobbies')
@login_required
def hobbies():
    form = HobbyForm()
    hobbies = current_user.hobbies
    return render_template('admin/hobbies/hobby.html', form=form, hobbies=hobbies, url=url_for('admin.add_hobby'))


@admin.route('/hobbies/add', methods=['POST'])
@login_required
def add_hobby():
    form = HobbyForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            hobby = Hobby(title=form.title.data, user_id=current_user.id)
            hobby.icon = form.icon.data
            hobby.description = form.description.data
            hobby.published = form.published.data
            repository.save(hobby)
            flash("Loisir ajouté avec succès", 'success')
            return redirect(url_for('admin.hobbies'))
        else:
            flash('Formulaire incorrect', 'error')
    else:
        return redirect(url_for('admin.add_hobby'))


@admin.route('/hobbies/edit/<uid>', methods=['GET', 'POST'])
@login_required
def edit_hobby(uid):
    hobbies = Hobby.query.all()
    hobby = Hobby.query.filter_by(uid=uid).first()
    form = HobbyForm(obj=hobby)

    if request.method == 'POST':
        if form.validate_on_submit:
            hobby.title = form.title.data
            hobby.icon = form.icon.data
            hobby.description = form.description.data
            hobby.published = form.published.data
            repository.save(hobby)
            flash("Loisir modifié avec succès", 'success')
            return redirect(url_for('admin.hobbies'))
        else:
            flash('Formulaire incorrect', 'error')
    return render_template('admin/hobbies/hobby.html', form=form, hobbies=hobbies,
                           url=url_for('admin.edit_hobby', uid=uid), hobby=hobby)


@admin.route('/hobbies/delete/<uid>')
@login_required
def delete_hobby(uid):
    hobby = Hobby.query.filter_by(uid=uid).first()
    repository.delete(hobby)
    flash("Loisir supprimé avec succès", 'success')
    return redirect(url_for('admin.hobbies'))
