from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, HiddenField, SubmitField, BooleanField
from wtforms.validators import ValidationError, Length, Email, DataRequired
from flask_babel import _
from app.models import User

class UserCreateForm(FlaskForm):
    username = StringField(_('Benutzername'), validators=[Length(max=128, message=_('Der Benutzername darf maximal 128 Zeichen lang sein.'))])
    firstname = StringField(_('Vorname'), validators=[Length(max=256, message=_('Maximal 256 Zeichen für Vorname(n) erlaubt.'))])
    lastname = StringField(_('Nachname'), validators=[Length(max=256, message=_('Maximal 256 Zeichen für Nachname(n) erlaubt.'))])
    email = StringField(_('E-Mail-Adresse'), validators=[Length(max=256, message=_('Die E-Mail-Adresse darf maximal 256 Zeichen lang sein.')), Email(_('Ungültige E-Mail-Adresse'))])
    phone = StringField(_('Telefonnummer'), validators=[Length(max=256, message=_('Die Telefonnummer darf maximal 256 Zeichen lang sein.'))])

    is_admin = BooleanField(_('Administrator'), default=False)
    login_allowed = BooleanField(_('Darf sich einloggen'), default=True)
    create_calendar_entry = BooleanField(_('Darf Kalendereinträge anlegen'), default=False)
    create_user = BooleanField(_('Darf Benutzer anlegen'), default=False)
    edit_user = BooleanField(_('Darf Benutzer bearbeiten'), default=False)
    delete_user = BooleanField(_('Darf Benutzer löschen'), default=False)
    edit_rights = BooleanField(_('Darf Benutzerrechte bearbeiten'), default=False)
    create_post = BooleanField(_('Darf Nachrichten schreiben'), default=True)
    edit_foreign_post = BooleanField(_('Darf fremde Nachrichten bearbeiten'), default=False)
    delete_foreign_post = BooleanField(_('Darf fremde Nachrichten löschen'), default=False)

    submit = SubmitField(_('Benutzer anlegen'))

    def validate_username(self, username):
        if username.data.strip(' \t\n\r') == '':
            raise ValidationError(_('Der Benutzername darf nicht leer sein.'))

    def validate_email(self, email):
        if email.data.strip(' \t\n\r') == '':
            raise ValidationError(_('Die E-Mail-Adresse darf nicht leer sein.'))
        check_email = User.query.filter_by(email=email.data).first()
        if check_email is not None:
            self.email.errors.append(_('Diese E-Mail-Adresse ist bereits registriert.'))
            return False
        return True

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

class UserDeleteForm(FlaskForm):
    safety = BooleanField(_('Ich bin mir sicher, dass ich diesen Benutzer löschen möchte.'), validators=[DataRequired(_('Du musst bestätigen, dass du den Benutzer löschen möchtest.'))])
    submitdelete = SubmitField(_('Benutzer löschen'))

class GenerateNew2FAForm(FlaskForm):
    safety2fa = BooleanField(_('Ich bin mir sicher, dass ich ein neues 2FA-Geheimnis generieren möchte.'), validators=[DataRequired(_('Du musst bestätigen, dass du das Geheimnis neu erzeugen möchtest.'))])
    submitnew2fa = SubmitField(_('Neues Geheimnis generieren'))