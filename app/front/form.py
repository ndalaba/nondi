from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email


class EmailForm(Form):
    user = StringField()
    name = StringField('Nom', validators=[DataRequired('Veillez renseigner un nom')])
    subject = StringField('Sujet', validators=[DataRequired('Veillez renseigner le sujet')])
    email = StringField('Email', validators=[DataRequired('Veillez renseigner un mail'), Email('Adresse mail incorrecte')])
    message = TextAreaField('Message', validators=[DataRequired('Veillez renseigner le message')])
