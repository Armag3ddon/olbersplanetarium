from flask import redirect, url_for, render_template, flash, request, current_app, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _
import sqlalchemy as sa
from app import db
from app.models import User
from app.auth import bp
from app.auth.forms import LoginForm, VerifyForm, TwoFactorSetupForm, TwoFactorVerifyForm
from app.email.mail_utils import verify_token
from app.misc.utils import generate_qr_code
import pyotp

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
        if user.is2fa_enabled:
            session['pre_2fa_userid'] = user.id
            session['remember_me'] = form.remember_me.data
            return redirect(url_for('auth.verify_2fa'))
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
    if not token and not current_app.config.get('DEBUG'):
        flash(_('Kein Sicherheitstoken angegeben!'))
        return redirect(url_for('auth.login'))

    if current_app.config.get('DEBUG'):
        flash(_('Debug-Modus aktiviert! Sicherheitstoken wird nicht überprüft.'))
    else:
        report, email = verify_token(token, current_app.config['SECRET_KEY'], 'email-registration', 86400)
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
            return redirect(url_for('auth.setup_2fa'))
        return redirect(url_for('main.startpage'))
    return render_template('auth/verify.html', title=_('Verifizierung'), form=form)

# SETTING UP TWO FACTOR AUTHENTICATION
@bp.route('/setup-2fa', methods=['GET', 'POST'])
@login_required
def setup_2fa():
    id = request.args.get('user')
    # Default: look at oneself
    if not id:
        id = current_user.id
    user = current_user
    if id != current_user.id:
        if not current_user.check_right_or_admin('edit_user'):
            flash(_('Du hast keine Berechtigung, die 2FA für andere Benutzer einzurichten!'))
            return redirect(url_for('main.startpage'))
        user = db.session.scalar(sa.select(User).where(User.id == id))
    secret = user.token_2fa
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name = user.username, issuer_name=current_app.config['APP_NAME'])
    qr_code = generate_qr_code(uri)
    form = TwoFactorSetupForm()
    if form.validate_on_submit():
        if not pyotp.TOTP(secret).verify(form.token.data):
            flash(_('Ungültiger OTP! Bitte versuche es erneut.'))
            return render_template('auth/setup_2fa.html', title=_('2FA einrichten'), qr_code=qr_code, secret=secret, form=form, username=user.username)
        user.is2fa_enabled = True
        db.session.commit()
        flash(_('Zwei-Faktor-Authentifizierung erfolgreich eingerichtet!'))
        return redirect(url_for('main.startpage'))
    return render_template('auth/setup_2fa.html', title=_('2FA einrichten'), qr_code=qr_code, secret=secret, form=form, username=user.username)

# VERIFYING TWO FACTOR AUTHENTICATION
@bp.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    if 'pre_2fa_userid' not in session:
        flash(_('Die Zwei-Faktor-Authentifizierung kann nur durchgeführt werden, wenn du dich zuerst anmeldest!'))
        return redirect(url_for('auth.login'))
    user = db.session.get(User, session['pre_2fa_userid'])
    if user is None or not user.is2fa_enabled:
        flash(_('Ungültiger Benutzer oder Zwei-Faktor-Authentifizierung nicht aktiviert!'))
        return redirect(url_for('auth.login'))
    form = TwoFactorVerifyForm()
    if form.validate_on_submit():
        if not pyotp.TOTP(user.token_2fa).verify(form.token.data):
            flash(_('Ungültiges OTP! Bitte versuche es erneut.'))
            return redirect(url_for('auth.verify_2fa'))
        login_user(user, remember=session.get('remember_me', False))
        session.pop('pre_2fa_userid', None)
        session.pop('remember_me', None)
        return redirect(url_for('main.startpage'))
    return render_template('auth/verify_2fa.html', title=_('2FA Verifizierung'), form=form)