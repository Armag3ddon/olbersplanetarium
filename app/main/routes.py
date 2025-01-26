from flask import render_template
from flask_login import login_required
from flask_babel import _
from app.main import bp

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