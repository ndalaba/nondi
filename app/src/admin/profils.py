from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from app.src.admin.forms import UserForm, PasswordForm
from app.src.repository.Repository import Repository
from app.src.utils.upload import uploadImage
from . import admin


@admin.route('/home')
@admin.route('/')
@login_required
def home():
    return redirect(url_for('admin.profil'))
    #return render_template('admin/home.html',page='dashboard')


@admin.route('/profils')
def profil():
    form = UserForm(obj=current_user)
    password_form = PasswordForm()
    return render_template('admin/profils/profil.html', form=form, passwordForm=password_form)


@admin.route('/edit_profil', methods=['POST'])
@login_required
def edit_profil():

    form = UserForm(obj=current_user)
    
    if request.method == 'POST':
        if form.validate_on_submit:
            if form.photo.data and form.photo.data!=current_user.photo:
                image = uploadImage(form.photo.data,'upload/users/')
                current_user.photo= image

            current_user.name=form.name.data
            current_user.email=form.email.data
            current_user.phone=form.phone.data
            current_user.facebook=form.facebook.data
            current_user.location=form.location.data
            Repository.save(current_user)
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
            Repository.save(current_user)
            flash('Mot de passe modifié avec succès','success')
            return redirect(url_for('admin.profil'))
        
        else:
            flash('Les champs du formulaire ne sont pas bien remplis','error')
    else:
        return redirect(url_for('admin.profil'))
