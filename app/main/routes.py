from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from flask_babel import _
from markupsafe import escape
from app.main import bp
from app import db
from app.models import CalendarEntry, Post
from app.main.forms import EventCreationForm, PostCreationForm
import calendar as cal
import sqlalchemy as sa
import datetime as dt

# STARTPAGE
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/start', methods=['GET', 'POST'])
@bp.route('/startpage', methods=['GET', 'POST'])
@login_required
def startpage():
    # Check access rights
    if current_user.check_right_or_admin('create_calendar_entry') == False:
        form = None
    else:
        form = PostCreationForm()
    if form and form.validate_on_submit():
        now = dt.datetime.now()
        answer_to = None
        if form.answer_to.data != "":
            try:
                answer_to = int(form.answer_to.data)
            except:
                flash(_('Fehler: Fehlerhafte Daten zur beantworteten Nachricht.'))
                return redirect(url_for('main.startpage'))
        if answer_to != None:
            answered = db.session.scalars(sa.select(Post).where(Post.id == answer_to)).first()
            if answered == None:
                flash(_('Fehler: Die beantwortete Nachricht existiert nicht.'))
                return redirect(url_for('main.startpage'))
            post = Post(
                title=escape(form.title.data),
                content=escape(form.content.data),
                timestamp=now,
                user_id=current_user.id,
                answer_to=answered.id)
        else:
            post = Post(
                title=escape(form.title.data),
                content=escape(form.content.data),
                timestamp=now,
                user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash(_('Beitrag erfolgreich erstellt.'))
        return redirect(url_for('main.startpage'))
    return render_template('main/startpage.html', title=_("Startseite - "), form=form)

# POST QUERYING
@bp.route('/posts/<page>', methods=['GET'])
@login_required
def posts(page):
    limit = 2
    if request.args.get('post') != None:
        query = db.session.scalars(sa.select(Post).where(Post.id == page))
        limit = 30
    else:
        page = int(page)-1
        if page < 0:
            page = 0
        query = db.session.scalars(sa.select(Post).where(Post.answer_to == None).order_by(Post.timestamp.desc()).limit(10).offset(10*page))
    result = { "posts": [], "answers": [] }

    for p in query:
        result["posts"].append({ 'id': p.id, 'title': p.title, 'content': p.content, 'timestamp': p.timestamp, 'author': p.user.username, 'author_avatar': p.user.avatar })
        answers_query = db.session.scalars(sa.select(Post).where(Post.answer_to == p.id).order_by(Post.timestamp.desc()).limit(limit))
        temp = [ { 'id': a.id, 'answer_to': a.answer_to, 'title': a.title, 'content': a.content, 'timestamp': a.timestamp, 'author': a.user.username, 'author_avatar': a.user.avatar } for a in answers_query ]
        result["answers"] += temp
    return result

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
    # Check access rights
    if current_user.check_right_or_admin('create_calendar_entry') == False:
        flash(_('Fehler: Keine Berechtigung zur Erstellung von Kalendereinträgen.'))
        return redirect(url_for('main.calendar'))
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