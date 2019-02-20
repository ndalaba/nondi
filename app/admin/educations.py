from flask_login import login_required,current_user
from flask import render_template, redirect, request, flash,url_for
from . import admin
from app.repository.Repository import repository
from app.entity.Entities import Education
from .forms import Education as EducationForm


@admin.route('/educations')
@login_required
def educations():
    form = EducationForm()
    educations = current_user.educations
    return render_template('admin/educations/education.html',form=form,educations=educations,url=url_for('admin.add_education'))


@admin.route('/educations/add',methods=['POST'])
@login_required
def add_education():
    form = EducationForm()
    if request.method=='POST':
        if form.validate_on_submit:
            education = Education(formation=form.formation.data,user_id=current_user.id)
            education.location= form.location.data
            education.school= form.school.data
            education.begin_at=form.begin_at.data
            education.end_at= form.end_at.data
            education.description= form.description.data
            education.published= form.published.data
            repository.save(education)
            flash("Formation ajoutée avec succès",'success')
            return redirect(url_for('admin.educations'))
        else:
            flash('Formulaire incorrect','error')
    else:
        return redirect(url_for('admin.add_education'))


@admin.route('/educations/edit/<uid>',methods=['GET','POST'])
@login_required
def edit_education(uid):
    educations = current_user.educations
    education= Education.query.filter_by(uid=uid).first()
    form = EducationForm(obj=education)

    if request.method=='POST':
        if form.validate_on_submit:
            education.formation=form.formation.data
            education.location= form.location.data
            education.school= form.school.data
            education.begin_at=form.begin_at.data
            education.end_at= form.end_at.data
            education.description= form.description.data
            education.published= form.published.data
            repository.save(education)
            flash("Formation modifié avec succès",'success')
            return redirect(url_for('admin.educations'))
        else:
            flash('Formulaire incorrect','error')
    return render_template('admin/educations/education.html', form=form, educations=educations,url=url_for('admin.edit_education',uid=uid),education=education)


@admin.route('/educations/delete/<uid>')
@login_required
def delete_education(uid):
    education= Education.query.filter_by(uid=uid).first()
    repository.delete(education)
    flash("Formation supprimée avec succès",'success')
    return redirect(url_for('admin.educations'))