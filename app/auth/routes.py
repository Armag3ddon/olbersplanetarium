from flask import redirect, url_for, render_template, flash
from flask_login import current_user, login_user, logout_user
from flask_babel import _
import sqlalchemy as sa
from app import db
from app.models import User
from app.auth import bp
from app.auth.forms import LoginForm

# LOGIN
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Logged in users get redirected
    if current_user.is_authenticated:
        return redirect(url_for('main.startpage'))
    # Load login form
    form = LoginForm()
    # Check form submission
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash(_('Benutzername oder Passwort falsch!'))
            return redirect(url_for('auth.login'))
        # Specifically use check_right and not check_right_or_admin
        if not user.check_right('login_allowed'):
            flash(_('Login nicht erlaubt!'))
            return redirect(url_for('auth.login'))
        # Login
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.startpage'))
    return render_template('auth/login.html', title=_('Login'), form=form)

# LOGOUT
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))