# coding: utf-8
# Login form

from flask_wtf import Form
from wtforms import StringField, validators,  PasswordField, SubmitField,BooleanField


class LoginForm(Form):
    email = StringField("Email", [validators.Required("Veillez renseigner le champ email"), validators.Email('Renseigner une adresse mail valide')])
    password = PasswordField('Mot de passe', [validators.Required('Veillez renseigner un mot de passe')])
    remember_me= BooleanField('Rester connecte')
    submit = SubmitField('Se connecter')


class PasswordForm(Form):
    last_password=PasswordField('Ancien mot de passe',[validators.Required('Veillez renseigner l\'ancien mot de passe')])
    password = PasswordField('Password',[validators.Required(),validators.EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Modifier')
