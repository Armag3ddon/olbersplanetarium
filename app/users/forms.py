from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import ValidationError, Length, Email, DataRequired
from flask_babel import _
from app.models import User

class UserEditForm(FlaskForm):
    id = HiddenField(validators=[DataRequired(_('Benutzer-ID nicht übertragen.')), ])
    username = StringField(_('Benutzername'), validators=[Length(max=128, message=_('Der Benutzername darf maximal 128 Zeichen lang sein.'))])
    firstname = StringField(_('Vorname'), validators=[Length(max=256, message=_('Maximal 256 Zeichen für Vorname(n) erlaubt.'))])
    lastname = StringField(_('Nachname'), validators=[Length(max=256, message=_('Maximal 256 Zeichen für Nachname(n) erlaubt.'))])
    email = StringField(_('E-Mail-Adresse'), validators=[Length(max=256, message=_('Die E-Mail-Adresse darf maximal 256 Zeichen lang sein.')), Email(_('Ungültige E-Mail-Adresse'))])
    phone = StringField(_('Telefonnummer'), validators=[Length(max=256, message=_('Die Telefonnummer darf maximal 256 Zeichen lang sein.'))])

    avatar = FileField(_('Profilbild'), validators=[FileAllowed(['jpg', 'png'], _('Nur .jpg und .png Dateien erlaubt.'))])
    submit = SubmitField(_('Speichern'))

    def validate(self, extra_validators=None, *args, **kwargs):
        success = super().validate(extra_validators, *args, **kwargs)
        check_username = User.query.filter_by(username=self.username.data).first()
        if check_username is not None:
            if check_username.id != int(self.id.data):
                self.username.errors.append(_('Dieser Benutzername ist bereits vergeben.'))
                success = False
        check_email = User.query.filter_by(email=self.email.data).first()
        if check_email is not None:
            if check_email.id != int(self.id.data):
                self.email.errors.append(_('Diese E-Mail-Adresse ist bereits registriert.'))
                success = False
        return success

    def validate_username(self, username):
        if username.data.strip(' \t\n\r') == '':
            raise ValidationError(_('Der Benutzername darf nicht leer sein.'))