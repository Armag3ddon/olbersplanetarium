from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length
from flask_babel import _

class LoginForm(FlaskForm):
    username = StringField(_('Benutzername'), validators=[InputRequired(_('Feld muss ausgefüllt werden'))])
    password = PasswordField(_('Passwort'), validators=[InputRequired(_('Feld muss ausgefüllt werden'))])
    remember_me = BooleanField(_('Eingeloggt bleiben'))
    submit = SubmitField(_('Einloggen'))

class VerifyForm(FlaskForm):
    password = PasswordField(_('Passwort'), validators=[InputRequired(_('Feld muss ausgefüllt werden'))])
    confirm_password = PasswordField(_('Passwort bestätigen'), validators=[InputRequired(_('Feld muss ausgefüllt werden')), EqualTo('password', message=_('Passwörter müssen übereinstimmen'))])
    tfa = BooleanField(_('Zwei-Faktor-Authentifizierung aktivieren'))
    submit = SubmitField(_('Passwort setzen'))

class TwoFactorSetupForm(FlaskForm):
    token = StringField(_('OTP aus dem Authenticator hier einfügen:'), validators=[InputRequired(_('OTP muss hier eingetragen werden')), Length(min=6, max=6)])
    submit = SubmitField(_('Einrichtung abschließen'))

class TwoFactorVerifyForm(FlaskForm):
    token = StringField(_('OTP hier eingeben:'), validators=[InputRequired(_('OTP muss hier eingetragen werden')), Length(min=6, max=6)])
    submit = SubmitField(_('Verifizieren'))