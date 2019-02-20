from flask_login import login_required, current_user
from flask import render_template, redirect, request, flash, url_for
from . import admin
from app.repository.Repository import repository
from app.entity.Entities import Service
from .forms import Service as ServiceForm


@admin.route('/services')
@login_required
def services():
    form = ServiceForm()
    services = current_user.services
    return render_template('admin/services/service.html', form=form, services=services, url=url_for('admin.add_service'))


@admin.route('/services/add', methods=['POST'])
@login_required
def add_service():
    form = ServiceForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            service = Service(service=form.service.data, user_id=current_user.id)
            service.icon = form.icon.data
            service.description = form.description.data
            service.detail = form.detail.data
            service.published = form.published.data
            repository.save(service)
            flash("Service ajouté avec succès", 'success')
            return redirect(url_for('admin.services'))
        else:
            flash('Formulaire incorrect', 'error')
    else:
        return redirect(url_for('admin.add_service'))


@admin.route('/services/edit/<uid>', methods=['GET', 'POST'])
@login_required
def edit_service(uid):
    services = current_user.services
    service = Service.query.filter_by(uid=uid).first()
    form = ServiceForm(obj=service)

    if request.method == 'POST':
        if form.validate_on_submit:
            service.service = form.service.data
            service.icon = form.icon.data
            service.detail = form.detail.data
            service.description = form.description.data
            service.published = form.published.data
            repository.save(service)
            flash("Service modifié avec succès", 'success')
            return redirect(url_for('admin.services'))
        else:
            flash('Formulaire incorrect', 'error')
    return render_template('admin/services/service.html', form=form, services=services, url=url_for('admin.edit_service', uid=uid), service=service)


@admin.route('/services/delete/<uid>')
@login_required
def delete_service(uid):
    service = Service.query.filter_by(uid=uid).first()
    repository.delete(service)
    flash("Service supprimé avec succès", 'success')
    return redirect(url_for('admin.services'))
