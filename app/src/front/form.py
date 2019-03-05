from flask_wtf import Form
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email


class EmailForm(Form):
    user = StringField()
    name = StringField('Nom', validators=[DataRequired('Veillez renseigner un nom')])
    subject = StringField('Sujet', validators=[DataRequired('Veillez renseigner le sujet')])
    email = StringField('Email', validators=[DataRequired('Veillez renseigner un mail'), Email('Adresse mail incorrecte')])
    message = TextAreaField('Message', validators=[DataRequired('Veillez renseigner le message')])


class UserForm(Form):
    name = StringField('Nom et prénom', validators=[DataRequired('Veillez renseigner le champ nom et prénom')])
    email = StringField('Email', validators=[DataRequired('Veillez renseigner le champ email'), Email('Champ email incorrect')])
    phone = StringField('Téléphone')
    facebook = StringField('Facebook', validators=[DataRequired('Veillez renseigner le champ facebook')])
    password = PasswordField('Mot de passe', validators=[DataRequired('Veillez renseigner le champ mot de passe')])
    location = TextAreaField('Adresse')
