from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from flask_babel import _
from app.calendar import bp
from app.models import CalendarEntry
from app import db
from app.calendar.forms import EventCreationForm, CalendarYearEditForm
from datetime import datetime
import calendar as cal
import sqlalchemy as sa
import json

# PAGES FOR THE CALENDAR
# CALENDAR VIEW, EVENT EDITING

# public: Öffentliche Veranstaltung
# school: Schulveranstaltung
# special: Sonderveranstaltung
# misc: Sonstige Veranstaltung
# public_holiday: Feiertage und Ferien
# vacation: Urlaubszeiten
CALENDAR_TYPES = {
    'public': 0,
    'school': 1,
    'special': 2,
    'misc': 3,
    'public_holiday': 4,
    'vacation': 5
}

# CALENDAR
@bp.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    can_create = False
    edit_year = False
    if current_user.check_right_or_admin('create_calendar_entry'):
        can_create = True
    if current_user.check_right_or_admin('edit_calendar_year'):
        edit_year = True
    return render_template('calendar/calendar.html', title=_("Kalender - "), can_create=can_create, edit_year=edit_year)

# EVENT QUERYING
@bp.route('/events/<year>/<month>', methods=['GET'])
@login_required
def events(year, month):
    year = int(year)
    month = int(month)
    last_day = cal.monthrange(year, month)[1]
    query = db.session.scalars(sa.select(CalendarEntry).where(sa.and_(CalendarEntry.start >= f"{year}-{month}-01", CalendarEntry.start <= f"{year}-{month}-{last_day}")))
    return { 'events': [ { 'id': e.id, 'title': e.title, 'start': e.start, 'end': e.end, 'type': e.type } for e in query ] }

# EVENT CREATION
@bp.route('/createevent', methods=['GET', 'POST'])
@login_required
def createevent():
    # Check access rights
    if current_user.check_right_or_admin('create_calendar_entry') == False:
        flash(_('Fehler: Keine Berechtigung zur Erstellung von Kalendereinträgen.'))
        return redirect(url_for('calendar.calendar'))
    # Load form
    form = EventCreationForm()
    # Check form submission
    if form.validate_on_submit():
        # Create new event
        type = 3
        if form.type.data == 'public':
            type = 0
        elif form.type.data == 'school':
            type = 1
        elif form.type.data == 'special':
            type = 2
        event = CalendarEntry(title=form.title.data, description=form.description.data, start=form.start.data, end=form.end.data, type=type)
        db.session.add(event)
        db.session.commit()
        return render_template('calendar/createevent.html', title=_('Neue Veranstaltung - '), form=form, success=True, eventyear=form.start.data.year, eventmonth=form.start.data.month-1)
    return render_template('calendar/createevent.html', title=_('Neue Veranstaltung - '), form=form, success=False)

# HOLIDAYS AND SCHOOL VACATIONS
@bp.route('/calendaryears', methods=['GET', 'POST'])
@login_required
def calendaryears():
    # Check access rights
    if current_user.check_right_or_admin('edit_calendar_year') == False:
        flash(_('Fehler: Keine Berechtigung zur Bearbeitung von Kalenderjahren.'))
        return redirect(url_for('calendar.calendar'))
    # Prepare form
    year = request.args.get('year', default=datetime.now().year, type=int)
    form = CalendarYearEditForm(year=str(year))
    form.year.choices = [(str(y), str(y)) for y in range(year-5, year+6)]
    # Check form submission
    if form.validate_on_submit():
        events = json.loads(form.days.data)
    return render_template('calendar/calendaryears.html', title=_('Ferienzeiten o.ä. bearbeiten - '), year=year, form=form)

# CALENDAR YEAR DATA QUERYING
@bp.route('/calendaryeardata/<year>', methods=['GET'])
@login_required
def calendaryeardata(year):
    year = int(year)
    query = db.session.scalars(sa.select(CalendarEntry).where(sa.and_(CalendarEntry.start >= f"{year}-01-01", CalendarEntry.start <= f"{year}-12-31", sa.or_(CalendarEntry.type == 4, CalendarEntry.type == 5))))
    return { 'events': [ { 'id': e.id, 'title': e.title, 'start': e.start, 'end': e.end, 'type': e.type } for e in query ] }