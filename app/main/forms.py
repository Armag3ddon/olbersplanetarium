from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, DateTimeLocalField, SelectField, SubmitField
from wtforms.validators import InputRequired, ValidationError, Length
from flask_babel import _

class EventCreationForm(FlaskForm):
    title = StringField(_('Veranstaltungstitel'), validators=[InputRequired(_('Feld muss ausgefüllt werden')), Length(max=256, message=_('Der Veranstaltungstitel darf maximal 256 Zeichen lang sein.'))])
    description = StringField(_('Beschreibung'))
    start = DateTimeLocalField(_('Beginn'), validators=[InputRequired(_('Feld muss ausgefüllt werden'))])
    end = DateTimeLocalField(_('Ende'), validators=[InputRequired(_('Feld muss ausgefüllt werden'))])
    type = SelectField(_('Veranstaltungstyp'), choices=[('public', _('Öffentliche Veranstaltung')), ('school', _('Schulveranstaltung')), ('special', _('Sonderveranstaltung')), ('misc', _('Sonstige Veranstaltung'))])
    submit = SubmitField(_('Eintragen'))

    def validate_start(self, start):
        if start.data >= self.end.data:
            raise ValidationError(_('Das Startdatum muss vor dem Enddatum liegen'))

class PostCreationForm(FlaskForm):
    title = StringField(_('Titel'), validators=[Length(max=256, message=_('Der Titel darf maximal 256 Zeichen lang sein.'))])
    content = HiddenField(validators=[Length(max=1024, message=_('Der Inhalt darf maximal 1024 Zeichen lang sein.'))])
    answer_to = HiddenField()
    submit = SubmitField(_('Abschicken'))