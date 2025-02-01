from flask import render_template, request
from flask_login import login_required
from flask_babel import _
from app.main import bp
from app import db
from app.models import CalendarEntry
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
    return render_template('main/calendar.html', title=_("Kalender - "))

# EVENTS
@bp.route('/events/<year>/<month>', methods=['GET'])
@login_required
def events(year, month):
    year = int(year)
    month = int(month)
    last_day = cal.monthrange(year, month)[1]
    query = db.session.scalars(sa.select(CalendarEntry).where(sa.and_(CalendarEntry.start >= f"{year}-{month}-01", CalendarEntry.start <= f"{year}-{month}-{last_day}")))
    return { 'events': [ { 'id': e.id, 'title': e.title, 'start': e.start, 'end': e.end } for e in query ] }