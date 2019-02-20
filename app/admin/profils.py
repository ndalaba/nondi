import random
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.admin.forms import UserForm, PasswordForm
from app.entity.Entities import Activity
from app.repository.Repository import repository
from app.utils.upload import uploadImage
from . import admin



@admin.route('/home')
@admin.route('/')
@login_required
def home():
    return redirect(url_for('admin.profil'))
    #return render_template('admin/home.html',page='dashboard')


@admin.route('activities/<uid>',methods=['POST','GET'])
@login_required
def activities(uid=None):
    if request.method=='POST':
        description=request.form['activity']
        activity= Activity(description=description,user_id=current_user.id)
        repository.save(activity)
        flash('Activité ajoutée avec succès','success')
    else: #suppression
        activity= Activity.query.filter_by(uid=uid).first()
        repository.delete(activity)
        flash('Activité supprimée avec succès','success')
       
    return redirect(url_for('admin.profil'))


@admin.route('/profils')
def profil():
    form= UserForm(obj=current_user)
    passwordForm= PasswordForm()
    activities=Activity.query.order_by(Activity.created_at.desc())
    colors = ['success', 'info', 'danger', 'warning', 'primary']
    return render_template('admin/profils/profil.html',form=form,activities=activities,passwordForm=passwordForm,random=random,colors=colors)


@admin.route('/edit_profil', methods=['POST'])
@login_required
def edit_profil():

    form= UserForm(obj=current_user)
    
    if request.method=='POST': 
        if form.validate_on_submit:
            if form.photo.data and form.photo.data!=current_user.photo:
                image = uploadImage(form.photo.data,'upload/users/')
                current_user.photo= image

            current_user.name=form.name.data
            current_user.email=form.email.data
            current_user.phone=form.phone.data
            current_user.job=form.job.data
            current_user.facebook=form.facebook.data
            current_user.twitter=form.twitter.data
            current_user.github=form.github.data
            current_user.linkedin=form.linkedin.data
            current_user.bio=form.bio.data
            current_user.location=form.location.data
            repository.save(current_user)
            flash('Compte mis à jour avec succès','success')
            return redirect(url_for('admin.profil'))
        
        else:
            flash('Les champs du formulaire ne sont pas bien remplis','error')
    else:
        return redirect(url_for('admin.profil'))


@admin.route('/edit_password', methods=['POST'])
@login_required
def edit_password():

    form= PasswordForm()
    
    if request.method=='POST': 
        if form.validate_on_submit:
            current_user.password=form.password.data
            repository.save(current_user)
            flash('Mot de passe modifié avec succès','success')
            return redirect(url_for('admin.profil'))
        
        else:
            flash('Les champs du formulaire ne sont pas bien remplis','error')
    else:
        return redirect(url_for('admin.profil'))
