from flask import render_template
from flask_login import login_required, current_user
from flask_babel import _
from app.main import bp
from app import db
from app.models import CalendarEntry
from app.main.forms import EventCreationForm
import calendar as cal
import sqlalchemy as sa

# STARTPAGE
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/start', methods=['GET', 'POST'])
@bp.route('/startpage', methods=['GET', 'POST'])
@login_required
def startpage():
    return render_template('main/startpage.html', title=_("Startseite - "))

# CALENDAR
@bp.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    can_create = False
    if current_user.check_right_or_admin('create_calendar_entry'):
        can_create = True
    return render_template('main/calendar.html', title=_("Kalender - "), can_create=can_create)

# EVENT QUERYING
@bp.route('/events/<year>/<month>', methods=['GET'])
@login_required
def events(year, month):
    year = int(year)
    month = int(month)
    last_day = cal.monthrange(year, month)[1]
    query = db.session.scalars(sa.select(CalendarEntry).where(sa.and_(CalendarEntry.start >= f"{year}-{month}-01", CalendarEntry.start <= f"{year}-{month}-{last_day}")))
    return { 'events': [ { 'id': e.id, 'title': e.title, 'start': e.start, 'end': e.end, 'public': e.public, 'school': e.school, 'special': e.special, 'misc': e.misc } for e in query ] }

# EVENT CREATION
@bp.route('/createevent', methods=['GET', 'POST'])
@login_required
def createevent():
    # Load form
    form = EventCreationForm()
    # Check form submission
    if form.validate_on_submit():
        # Create new event
        public = False
        school = False
        special = False
        misc = False
        if form.type.data == 'public':
            public = True
        elif form.type.data == 'school':
            school = True
        elif form.type.data == 'special':
            special = True
        elif form.type.data == 'misc':
            misc = True
        event = CalendarEntry(title=form.title.data, description=form.description.data, start=form.start.data, end=form.end.data, public=public, school=school, special=special, misc=misc)
        db.session.add(event)
        db.session.commit()
        return render_template('main/createevent.html', title=_('Neue Veranstaltung - '), form=form, success=True, eventyear=form.start.data.year, eventmonth=form.start.data.month-1)
    return render_template('main/createevent.html', title=_('Neue Veranstaltung - '), form=form, success=False)