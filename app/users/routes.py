from flask import render_template, redirect, url_for, flash, request, send_from_directory, current_app
from flask_login import login_required, current_user
from flask_babel import _
from app.users import bp
from app import db
from app.models import User
from app.users.forms import UserEditForm
import sqlalchemy as sa

# USERPAGE
@bp.route('/user', methods=['GET', 'POST'])
@login_required
def userpage():
    id = request.args.get('user')
    # Default: look at oneself
    if not id:
        id = current_user.id
    # Get user data
    user = current_user
    if id != current_user.id:
        user = db.session.scalar(sa.select(User).where(User.id == id))
        if user is None:
            flash(_('Fehler: Benutzer (ID: {}) nicht gefunden.'.format(id)))
            user = current_user
    # User editing
    edit = False
    form = None
    # Check access rights
    if edit and id != current_user.id:
        if current_user.check_right_or_admin('edit_user') == False:
            flash(_('Fehler: Keine Berechtigung zur Bearbeitung von fremden Benutzern.'))
            edit = False
    # Load edit form and populate with default values
    if request.args.get('edit'):
        edit = True
        form = UserEditForm(
            id=user.id,
            username=user.username,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            phone=user.phone
        )
    # Save user values
    if form and form.validate_on_submit():
        user.username = form.username.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.email = form.email.data
        user.phone = form.phone.data
        avatar = form.avatar.data
        if avatar:
            user.set_avatar(avatar)
        flash(_('Benutzerdaten gespeichert.'))
        db.session.commit()
        return redirect(url_for('users.userpage', user=user.id))
    return render_template('users/userpage.html', title=_("Benutzerübersicht - "), user=user, edit=edit, form=form)

# USER AVATARS
@bp.route('/avatar/<path:filename>', methods=['GET'])
@login_required
def avatar(filename):
    print(filename)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], path=filename)