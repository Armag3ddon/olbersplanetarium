from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import Length
from flask_babel import _

class PostCreationForm(FlaskForm):
    title = StringField(_('Titel'), validators=[Length(max=256, message=_('Der Titel darf maximal 256 Zeichen lang sein.'))])
    content = HiddenField(validators=[Length(max=1024, message=_('Der Inhalt darf maximal 1024 Zeichen lang sein.'))])
    answer_to = HiddenField()
    submit = SubmitField(_('Abschicken'))