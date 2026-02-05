from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from flask_babel import _
from markupsafe import escape
from app.main import bp
from app import db
from app.models import Post
from app.main.forms import PostCreationForm
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