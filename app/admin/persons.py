from flask_login import login_required
from flask import render_template, redirect, request, flash, url_for
from . import admin
from slugify import slugify
from app.repository.Repository import Repository
from app.entity.Person import Person
from .forms import Person as PersonForm
from app.utils.upload import uploadImage
from app.utils.auth import is_admin


@admin.route('/persons')
@is_admin
@login_required
def persons():
    form = PersonForm()
    persons = Person.query.all()
    return render_template('admin/persons/persons.html', form=form, persons=persons, url=url_for('admin.add_person'))


@admin.route('/persons/add', methods=['POST'])
@is_admin
@login_required
def add_person():
    form = PersonForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            person = Person(name=form.name.data, slug=slugify(form.name.data))
            if form.image.data:
                image = uploadImage(form.image.data, 'upload/persons/')
                person.image = image
            person.function = form.function.data
            person.content = form.content.data
            person.published = form.published.data
            Repository.save(person)
            flash("Personne ajoutée avec succès", 'success')
            return redirect(url_for('admin.persons'))
        else:
            flash('Formulaire incorrect', 'error')
    else:
        return redirect(url_for('admin.add_person'))


@admin.route('/persons/edit/<uid>', methods=['GET', 'POST'])
@is_admin
@login_required
def edit_person(uid):
    persons = Person.query.all()
    person = Person.query.filter_by(uid=uid).first()
    form = PersonForm(obj=person)

    if request.method == 'POST':
        if form.validate_on_submit:
            if form.image.data and form.image.data != person.image:
                image = uploadImage(form.image.data, 'upload/persons/')
                person.image = image
            person.name = form.name.data
            slug_title = slugify(form.name.data)
            person.slug = slug_title
            person.function = form.function.data
            person.content = form.content.data
            person.published = form.published.data
            Repository.save(person)
            flash("Personne modifiée avec succès", 'success')
            return redirect(url_for('admin.persons'))
        else:
            flash('Formulaire incorrect', 'error')
    return render_template('admin/persons/persons.html', form=form, persons=persons, url=url_for('admin.edit_person', uid=uid), person=person)


@admin.route('/persons/delete/<uid>')
@is_admin
@login_required
def delete_person(uid):
    person = Person.query.filter_by(uid=uid).first()
    Repository.delete(person)
    flash("Personne supprimé avec succès", 'success')
    return redirect(url_for('admin.persons'))
