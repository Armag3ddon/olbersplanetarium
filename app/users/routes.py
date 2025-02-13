from flask import render_template
from flask_login import login_required, current_user
from flask_babel import _
from app.users import bp
from app import db
from app.models import User
import sqlalchemy as sa

# USERPAGE
@bp.route('/user', methods=['GET', 'POST'])
@login_required
def userpage():
    return render_template('users/userpage.html', title=_("Benutzerübersicht - "), user=current_user)