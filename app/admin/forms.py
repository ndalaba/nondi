from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, validators, TextAreaField, SubmitField, DateField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email


class UserForm(Form):
    name = StringField('Nom et prénom', validators=[DataRequired('Veillez renseigner le champ nom et prénom')])
    email = StringField('Email',validators=[DataRequired('Veillez renseigner le champ email'), Email('Champ email incorrect')])
    phone = StringField('Téléphone', validators=[DataRequired('Veillez renseigner le champ téléphone')])
    job = StringField('Fonction', [validators.Required('Veillez renseigner le champ fonction')])
    facebook = StringField('Facebook')
    twitter = StringField('Twitter')
    github = StringField('Github')
    linkedin = StringField('Linkedin')
    location = TextAreaField('Adresse')
    bio = TextAreaField('Biographie')
    photo = FileField('Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Valider')


class PasswordForm(Form):
    password = PasswordField('Mot de passe', [validators.Required(), validators.EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirmation mot de passe')
    submit = SubmitField('Modifier')


class Education(Form):
    formation = StringField('Titre', [validators.Required('Veillez renseigner le champ titre')])
    location = StringField('Lieu', [validators.Required('Veillez renseigner le champ lieu')])
    school = StringField('Etablissement', [validators.Required('Veillez renseigner le champ établissement')])
    begin_at = DateField('Début', [validators.Required('Veillez renseigner le champ début')])
    end_at = DateField('Fin', [validators.Required('Veillez renseigner le champ fin')])
    description = TextAreaField('Description')
    published = BooleanField('Publié')


class Job(Form):
    title = StringField('Titre', [validators.Required('Veillez renseigner le champ titre')])
    location = StringField('Lieu', [validators.Required('Veillez renseigner le champ lieu')])
    company = StringField('Entreprise', [validators.Required('Veillez renseigner le champ entreprise')])
    begin_at = DateField('Début', [validators.Required('Veillez renseigner le champ début')])
    end_at = DateField('Fin', [validators.Required('Veillez renseigner le champ fin')])
    description = TextAreaField('Description')
    published = BooleanField('Publié')


class Service(Form):
    service = StringField('Titre', [validators.Required('Veillez renseigner le champ titre')])
    icon = StringField('Icon', [validators.Required('Veillez renseigner le champ icon')])
    description = TextAreaField('Description')
    detail = TextAreaField('Détails')
    published = BooleanField('Publié')


class Hobby(Form):
    title = StringField('Titre', [validators.Required('Veillez renseigner le champ titre')])
    icon = StringField('Icon', [validators.Required('Veillez renseigner le champ icon')])
    description = TextAreaField('Description')
    published = BooleanField('Publié')


class Skill(Form):
    skill = StringField('Titre', [validators.Required('Veillez renseigner le champ titre')])
    level = StringField('Niveau', [validators.Required('Veillez renseigner le champ niveau')])
    experience = StringField("Année d'expérience", [validators.Required("Veillez renseigner le champ année d'expérience")])
    description = TextAreaField('Description')
    percent = StringField('Pourcentage')
    techno = StringField('Technologie')
    published = BooleanField('Publié')


class Work(Form):
    title = StringField('Titre', [validators.Required('Veillez renseigner le champ titre')])
    category = StringField('Catégorie', validators=[DataRequired('Veillez renseigner le champ catégorie')])
    techno = StringField('Technologie', [validators.Required('Veillez renseigner le champ technologie')])
    url = StringField('Lien')
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    published = BooleanField('Publié')
    description = TextAreaField('Description')
