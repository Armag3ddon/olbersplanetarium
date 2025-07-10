from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, EqualTo
from flask_babel import _

class LoginForm(FlaskForm):
    username = StringField(_('Benutzername', validators=[InputRequired(_('Feld muss ausgefüllt werden'))]))
    password = PasswordField(_('Passwort'), validators=[InputRequired(_('Feld muss ausgefüllt werden'))])
    remember_me = BooleanField(_('Eingeloggt bleiben'))
    submit = SubmitField(_('Einloggen'))

class VerifyForm(FlaskForm):
    password = PasswordField(_('Passwort'), validators=[InputRequired(_('Feld muss ausgefüllt werden'))])
    confirm_password = PasswordField(_('Passwort bestätigen'), validators=[InputRequired(_('Feld muss ausgefüllt werden')), EqualTo('password', message=_('Passwörter müssen übereinstimmen'))])
    tfa = BooleanField(_('Zwei-Faktor-Authentifizierung aktivieren'))
    submit = SubmitField(_('Passwort setzen'))