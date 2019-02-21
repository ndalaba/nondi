from flask_login import login_required
from flask import render_template, redirect, request, flash, url_for
from . import admin
from slugify import slugify
from app.repository.Repository import Repository
from app.entity.Page import Page
from .forms import Page as PageForm
from app.utils.upload import uploadImage
from app.utils.auth import is_admin


@admin.route('/pages')
@is_admin
@login_required
def pages():
    form = PageForm()
    pages = Page.query.all()
    return render_template('admin/pages/pages.html', form=form, pages=pages, url=url_for('admin.add_page'))


@admin.route('/pages/add', methods=['POST'])
@is_admin
@login_required
def add_page():
    form = PageForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            page = Page(title=form.title.data, slug=slugify(form.title.data))
            if form.image.data:
                image = uploadImage(form.image.data, 'upload/pages/')
                page.image = image
            page.content = form.content.data
            page.published = form.published.data
            Repository.save(page)
            flash("Page ajoutée avec succès", 'success')
            return redirect(url_for('admin.pages'))
        else:
            flash('Formulaire incorrect', 'error')
    else:
        return redirect(url_for('admin.add_page'))


@admin.route('/pages/edit/<uid>', methods=['GET', 'POST'])
@is_admin
@login_required
def edit_page(uid):
    pages = Page.query.all()
    page = Page.query.filter_by(uid=uid).first()
    form = PageForm(obj=page)

    if request.method == 'POST':
        if form.validate_on_submit:
            if form.image.data and form.image.data != page.image:
                image = uploadImage(form.image.data, 'upload/pages/')
                page.image = image
            page.title = form.title.data
            page.content = form.content.data
            page.published = form.published.data
            Repository.save(page)
            flash("Page modifiée avec succès", 'success')
            return redirect(url_for('admin.pages'))
        else:
            flash('Formulaire incorrect', 'error')
    return render_template('admin/pages/pages.html', form=form, pages=pages, url=url_for('admin.edit_page', uid=uid), page=page)


@admin.route('/pages/delete/<uid>')
@is_admin
@login_required
def delete_page(uid):
    page = Page.query.filter_by(uid=uid).first()
    Repository.delete(page)
    flash("Page supprimé avec succès", 'success')
    return redirect(url_for('admin.pages'))
