from flask import render_template, redirect, request, flash, url_for
from flask_login import login_required

from app.entity.Article import Category
from app.repository.Repository import Repository
from app.utils.auth import is_admin
from slugify import slugify
from . import admin
from .forms import Category as CategoryForm


@admin.route('/categories')
@is_admin
@login_required
def categories():
    form = CategoryForm()
    categories = Category.query.all()
    return render_template('admin/categories/categories.html', form=form, categories=categories,
                           url=url_for('admin.add_category'))


@admin.route('/categories/add', methods=['POST'])
@is_admin
@login_required
def add_category():
    form = CategoryForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            slug_title = slugify(form.title.data)
            category = Category(title=form.title.data, slug=slug_title)
            category.description = form.description.data
            Repository.save(category)
            flash("Categorie ajoutée avec succès", 'success')
            return redirect(url_for('admin.categories'))
        else:
            flash('Formulaire incorrect', 'error')
    else:
        return redirect(url_for('admin.add_category'))


@admin.route('/categories/edit/<uid>', methods=['GET', 'POST'])
@is_admin
@login_required
def edit_category(uid):
    categories = Category.query.all()
    category = Category.query.filter_by(uid=uid).first()
    form = CategoryForm(obj=category)

    if request.method == 'POST':
        if form.validate_on_submit:
            slug_title = slugify(form.title.data)
            category.title = form.title.data
            category.slug = slug_title
            category.description = form.description.data
            Repository.save(category)
            flash("Categorie modifiée avec succès", 'success')
            return redirect(url_for('admin.categories'))
        else:
            flash('Formulaire incorrect', 'error')
    return render_template('admin/categories/categories.html', form=form, categories=categories,
                           url=url_for('admin.edit_category', uid=uid), category=category)


@admin.route('/categories/delete/<uid>')
@is_admin
@login_required
def delete_category(uid):
    category = Category.query.filter_by(uid=uid).first()
    Repository.delete(category)
    flash("Categorie supprimée avec succès", 'success')
    return redirect(url_for('admin.categories'))
