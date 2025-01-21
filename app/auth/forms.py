from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import _

class LoginForm(FlaskForm):
    username = StringField(_('Benutzername', validators=[DataRequired()]))
    password = PasswordField(_('Passwort'), validators=[DataRequired()])
    remember_me = BooleanField(_('Eingeloggt bleiben'))
    submit = SubmitField('Einloggen')