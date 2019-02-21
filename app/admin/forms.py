from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, validators, TextAreaField, SubmitField,  BooleanField, PasswordField
from wtforms.validators import DataRequired, Email


class UserForm(Form):
    name = StringField('Nom et prénom', validators=[DataRequired('Veillez renseigner le champ nom et prénom')])
    email = StringField('Email',validators=[DataRequired('Veillez renseigner le champ email'), Email('Champ email incorrect')])
    phone = StringField('Téléphone', validators=[DataRequired('Veillez renseigner le champ téléphone')])
    facebook = StringField('Facebook')
    location = TextAreaField('Adresse')
    photo = FileField('Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Valider')


class PasswordForm(Form):
    password = PasswordField('Mot de passe', [validators.Required(), validators.EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirmation mot de passe')
    submit = SubmitField('Modifier')


class Category(Form):
    title = StringField('Titre', validators=[DataRequired('Veillez renseigner le tittre')])
    description = TextAreaField('Description')
    published = BooleanField('Publié')
