from flask_login import login_required, current_user
from flask import render_template, redirect, request, flash, url_for
from . import admin
from app.repository.Repository import repository
from app.entity.Entities import Job
from .forms import Job as JobForm


@admin.route('/jobs')
@login_required
def jobs():
    form = JobForm()
    jobs = current_user.jobs
    return render_template('admin/jobs/job.html', form=form, jobs=jobs, url=url_for('admin.add_job'))


@admin.route('/jobs/add', methods=['POST'])
@login_required
def add_job():
    form = JobForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            job = Job(title=form.title.data, user_id=current_user.id)
            job.location = form.location.data
            job.company = form.company.data
            job.begin_at = form.begin_at.data
            job.end_at = form.end_at.data
            job.description = form.description.data
            job.published = form.published.data
            repository.save(job)
            flash("Expérience professionnelle ajoutée avec succès", 'success')
            return redirect(url_for('admin.jobs'))
        else:
            flash('Formulaire incorrect', 'error')
    else:
        return redirect(url_for('admin.add_job'))


@admin.route('/jobs/edit/<uid>', methods=['GET', 'POST'])
@login_required
def edit_job(uid):
    jobs = current_user.jobs
    job = Job.query.filter_by(uid=uid).first()
    form = JobForm(obj=job)

    if request.method == 'POST':
        if form.validate_on_submit:
            job.title = form.title.data
            job.location = form.location.data
            job.company = form.company.data
            job.begin_at = form.begin_at.data
            job.end_at = form.end_at.data
            job.description = form.description.data
            job.published = form.published.data
            repository.save(job)
            flash("Expérience professionnelle modifié avec succès", 'success')
            return redirect(url_for('admin.jobs'))
        else:
            flash('Formulaire incorrect', 'error')
    return render_template('admin/jobs/job.html', form=form, jobs=jobs, url=url_for('admin.edit_job', uid=uid), job=job)


@admin.route('/jobs/delete/<uid>')
@login_required
def delete_job(uid):
    job = Job.query.filter_by(uid=uid).first()
    repository.delete(job)
    flash("Expérience professionnelle supprimée avec succès", 'success')
    return redirect(url_for('admin.jobs'))
