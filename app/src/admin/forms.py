from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, validators, TextAreaField, SubmitField,  BooleanField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, URL


class UserForm(Form):
    name = StringField('Nom et prénom', validators=[DataRequired('Veillez renseigner le champ nom et prénom')])
    email = StringField('Email',validators=[DataRequired('Veillez renseigner le champ email'), Email('Champ email incorrect')])
    phone = StringField('Téléphone')
    facebook = StringField('Facebook')
    location = TextAreaField('Adresse')
    photo = FileField('Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    activated = BooleanField('Activé')
    submit = SubmitField('Valider')


class PasswordForm(Form):
    password = PasswordField('Mot de passe', [validators.Required(), validators.EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirmation mot de passe')
    submit = SubmitField('Modifier')


class Category(Form):
    title = StringField('Titre', validators=[DataRequired('Veillez renseigner le tittre')])
    description = TextAreaField('Description')
    published = BooleanField('Publié')


class Article(Form):
    title = StringField('Titre', validators=[DataRequired('Veillez renseigner le titre de l\'article')])
    top = BooleanField('À la une')
    category = SelectField('Catégorie', coerce=int, validators=[DataRequired()])
    content = TextAreaField('Contenu')
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    published = BooleanField('Publié')


class Page(Form):
    title = StringField('Titre', validators=[DataRequired('Veillez renseigner le titre de la page')])
    content = TextAreaField('Contenu', validators=[DataRequired('Veillez renseigner le contenu de la page')])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    published = BooleanField('Publié')


class Person(Form):
    name = StringField('Nom', validators=[DataRequired('Veillez renseigner le nom')])
    fonction = StringField('Fonction', validators=[DataRequired('Veillez renseigner la fonction')])
    image = FileField('Photo', validators=[FileAllowed(['jpg','jpeg','png'])])
    content = TextAreaField('Description')
    published = BooleanField('Publié')


class Video(Form):
    title = StringField('Titre', validators=[DataRequired('Veillez renseigner le titre de la vidéo')])
    video = StringField('Lien vidéo', validators=[URL('Veillez renseigner le lien de la video')])
    category = SelectField('Catégorie', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Description')
    published = BooleanField('Publié')


