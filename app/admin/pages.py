from flask_login import login_required, current_user
from flask import render_template, redirect, request, flash, url_for
from . import admin
from app.repository.Repository import Repository
from app.entity.Entities import Page
from .forms import Page as PageForm


@admin.route('/pages')
@login_required
def pages():
    form = PageForm()
    pages = current_user.pages
    return render_template('admin/categories/page.html', form=form, pages=pages, url=url_for('admin.add_page'))


@admin.route('/pages/add', methods=['POST'])
@login_required
def add_page():
    form = PageForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            page = Page(page=form.page.data, user_id=current_user.id)
            page.icon = form.icon.data
            page.description = form.description.data
            page.detail = form.detail.data
            page.published = form.published.data
            repository.save(page)
            flash("Page ajouté avec succès", 'success')
            return redirect(url_for('admin.pages'))
        else:
            flash('Formulaire incorrect', 'error')
    else:
        return redirect(url_for('admin.add_page'))


@admin.route('/pages/edit/<uid>', methods=['GET', 'POST'])
@login_required
def edit_page(uid):
    pages = current_user.pages
    page = Page.query.filter_by(uid=uid).first()
    form = PageForm(obj=page)

    if request.method == 'POST':
        if form.validate_on_submit:
            page.page = form.page.data
            page.icon = form.icon.data
            page.detail = form.detail.data
            page.description = form.description.data
            page.published = form.published.data
            repository.save(page)
            flash("Page modifié avec succès", 'success')
            return redirect(url_for('admin.pages'))
        else:
            flash('Formulaire incorrect', 'error')
    return render_template('admin/categories/page.html', form=form, pages=pages, url=url_for('admin.edit_page', uid=uid), page=page)


@admin.route('/pages/delete/<uid>')
@login_required
def delete_page(uid):
    page = Page.query.filter_by(uid=uid).first()
    repository.delete(page)
    flash("Page supprimé avec succès", 'success')
    return redirect(url_for('admin.pages'))
