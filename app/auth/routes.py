from flask import redirect, url_for, render_template, flash, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _
import sqlalchemy as sa
from app import db
from app.models import User
from app.auth import bp
from app.auth.forms import LoginForm, VerifyForm
from app.mail.mail_utils import verify_token

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

# VERFICATION AND PASSWORD ENTRY
@bp.route('/verify', methods=['GET', 'POST'])
def verify():
    token = request.args.get('token')
    if not token:
        flash(_('Kein Sicherheitstoken angegeben!'))
        return redirect(url_for('auth.login'))

    report, email = verify_token(token, current_app.config['SECRET_KEY'], 'email-registration')
    if report != True:
        flash(email)
        return redirect(url_for('auth.login'))

    user = db.session.scalar(sa.select(User).where(User.email == email))
    if user is None:
        flash(_('Benutzer mit dieser E-Mail-Adresse nicht gefunden!'))
        return redirect(url_for('auth.login'))

    flash(_('E-Mail-Adresse erfolgreich verifiziert!'))
    form = VerifyForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash(_('Passwörter stimmen nicht überein!'))
            return redirect(url_for('auth.verify', token=token))
        if not user.set_password(form.password.data):
            flash(_('Passwort konnte nicht gesetzt werden!'))
            return redirect(url_for('auth.verify', token=token))
        db.session.commit()
        flash(_('Passwort erfolgreich gesetzt! Du kannst dich jetzt einloggen.'))
        login_user(user)
        if form.tfa.data:
            return redirect(url_for('auth.setup-2fa'))
        return redirect(url_for('main.startpage'))
    return redirect(url_for('auth.login'))

@bp.route('/setup-2fa')
@login_required
def setup_2fa():
    return redirect(url_for('main.startpage'))