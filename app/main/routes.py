from flask import render_template
from flask_babel import _
from app.main import bp

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def startpage():
    return render_template('main/main.html', title=_("Startseite - "))