from flask_login import login_required, current_user
from flask import render_template, redirect, request, flash, url_for
from . import admin
from app.repository.Repository import repository
from app.entity.Entities import Work
from .forms import Work as WorkForm
from app.utils.upload import uploadImage


@admin.route('/works')
@login_required
def works():
    form = WorkForm()
    works = current_user.works #Work.query.all()
    return render_template('admin/works/work.html', form=form, works=works, url=url_for('admin.add_work'))


@admin.route('/works/add', methods=['POST'])
@login_required
def add_work():
    form = WorkForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            work = Work(title=form.title.data, user_id=current_user.id)
            if form.image.data:
                image = uploadImage(form.image.data, 'upload/works/')
                work.image = image
            work.techno = form.techno.data
            work.category = form.category.data
            work.url = form.url.data
            work.description = form.description.data
            work.published = form.published.data
            repository.save(work)
            flash("Réalisation ajoutée avec succès", 'success')
            return redirect(url_for('admin.works'))
        else:
            flash('Formulaire incorrect', 'error')
    else:
        return redirect(url_for('admin.add_work'))


@admin.route('/works/edit/<uid>', methods=['GET', 'POST'])
@login_required
def edit_work(uid):
    works = current_user.works  #Work.query.all()
    work = Work.query.filter_by(uid=uid).first()
    form = WorkForm(obj=work)

    if request.method == 'POST':
        if form.validate_on_submit:
            if form.image.data and form.image.data != work.image:
                image = uploadImage(form.image.data, 'upload/works/')
                work.image = image
            work.title = form.title.data
            work.techno = form.techno.data
            work.category = form.category.data
            work.url = form.url.data
            work.description = form.description.data
            work.published = form.published.data
            repository.save(work)
            flash("Réalisation modifiée avec succès", 'success')
            return redirect(url_for('admin.works'))
        else:
            flash('Formulaire incorrect', 'error')
    return render_template('admin/works/work.html', form=form, works=works, url=url_for('admin.edit_work', uid=uid), work=work)


@admin.route('/works/delete/<uid>')
@login_required
def delete_work(uid):
    work = Work.query.filter_by(uid=uid).first()
    repository.delete(work)
    flash("Réalisation supprimée avec succès", 'success')
    return redirect(url_for('admin.works'))
