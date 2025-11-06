from flask import render_template, redirect, url_for, flash, request, send_from_directory, current_app
from flask_login import login_required, current_user
from flask_babel import _
from app.users import bp
from app import db
from app.models import User, Right
from app.users.forms import UserEditForm, GenerateNew2FAForm, UserDeleteForm, UserCreateForm
from app.email.mail_utils import generate_token, send_email
import sqlalchemy as sa
import pyotp

# USERPAGE
@bp.route('/user', methods=['GET', 'POST'])
@login_required
def userpage():
    id = request.args.get('user')
    rights = get_user_rights()
    # This will be set to true if the user id not found
    # In this case the id will default to the current user
    # This could lead to erroneous deletion or alteration of own user
    error_prevention = False
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
            error_prevention = True
    # User editing
    edit = False
    if request.args.get('edit'):
        edit = True
    editform = None
    change2faform = None
    deleteform = None
    # Check access rights
    if edit and id != current_user.id:
        if rights['edit_users'] == False:
            flash(_('Fehler: Keine Berechtigung zur Bearbeitung von fremden Benutzern.'))
            edit = False
    # Load edit form and populate with default values
    if edit and not error_prevention:
        editform = UserEditForm(
            id=user.id,
            username=user.username,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            phone=user.phone
        )
        change2faform = GenerateNew2FAForm()
        if rights['delete_users']:
            deleteform = UserDeleteForm()
    # Save user values
    if editform and editform.submit.data and editform.validate_on_submit():
        user.username = editform.username.data
        user.firstname = editform.firstname.data
        user.lastname = editform.lastname.data
        user.email = editform.email.data
        user.phone = editform.phone.data
        avatar = editform.avatar.data
        if avatar:
            user.set_avatar(avatar)
        flash(_('Benutzerdaten gespeichert.'))
        db.session.commit()
        return redirect(url_for('users.userpage', user=user.id))
    # Generate new 2FA secret
    if change2faform and change2faform.submitnew2fa.data and change2faform.validate_on_submit():
        user.token_2fa = pyotp.random_base32()
        user.is2fa_enabled = False
        flash(_('Neues Geheimnis für die Zwei-Faktor-Authentifizierung generiert. Bitte richte 2FA erneut ein.'))
        db.session.commit()
        return redirect(url_for('auth.setup_2fa', user=user.id))
    # Delete user
    if deleteform and deleteform.submitdelete.data and deleteform.validate_on_submit():
        if user.id == current_user.id:
            flash(_('Fehler: Du kannst dich nicht selbst löschen!'))
            return redirect(url_for('users.userpage', user=user.id))
        # Purge rights
        db.session.query(Right).filter(Right.user_id == user.id).delete()
        # Delete user
        db.session.delete(user)
        db.session.commit()
        flash(_('Benutzer {} gelöscht.'.format(user.username)))
        return redirect(url_for('users.userlist', page=1))
    return render_template('users/userpage.html', title=_("Benutzerübersicht - "), user=user, edit=edit, editform=editform, change2faform=change2faform, deleteform=deleteform, rights=rights)

# USERLIST
@bp.route('/userlist/<page>', methods=['GET'])
@login_required
def userlist(page):
    rights = get_user_rights()
    query = sa.Select(User).order_by(User.id)
    users = db.paginate(query, page=int(page), per_page=50, error_out=False)
    next_url = url_for('users.userlist', page=users.next_num) if users.has_next else None
    prev_url = url_for('users.userlist', page=users.prev_num) if users.has_prev else None
    return render_template('users/userlist.html', title=_("Benutzerliste - "), users=users.items, next_url=next_url, prev_url=prev_url, rights=rights, can_edit=rights['delete_users'])

# USER CREATION
@bp.route('/usercreate', methods=['GET', 'POST'])
@login_required
def usercreate():
    rights = get_user_rights()
    # Check access rights
    if not rights['create_users']:
        flash(_('Fehler: Keine Berechtigung zur Erstellung von Benutzern.'))
        return redirect(url_for('users.userlist', page=1))
    form = UserCreateForm()
    # Create new user
    if form.validate_on_submit():
        # Submit the user
        user = User(
            username=form.username.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data,
            phone=form.phone.data,
            token_2fa=pyotp.random_base32()
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        # Submit the user rights
        rights = Right(
            user_id=user.id,
            is_admin=form.is_admin.data,
            login_allowed=form.login_allowed.data,
            create_calendar_entry=form.create_calendar_entry.data,
            create_user=form.create_user.data,
            edit_user=form.edit_user.data,
            delete_user=form.delete_user.data,
            edit_rights=form.edit_rights.data,
            create_post=form.create_post.data,
            edit_foreign_post=form.edit_foreign_post.data,
            delete_foreign_post=form.delete_foreign_post.data
        )
        db.session.add(rights)
        db.session.commit()
        flash_message = _('Benutzer {} erstellt.'.format(user.username))

        # Create and send the registration token
        token = generate_token(form.email.data, current_app.config['SECRET_KEY'], 'email-registration')
        verify_url = url_for('auth.verify', token=token, _external=True)
        report = send_email(
            to=form.email.data,
            subject=_('Willkommen beim Olbers Planetarium'),
            template='auth/mail_registration',
            verify_url=verify_url
        )
        flash_message += report

        flash(flash_message)
        return redirect(url_for('users.userlist', page=1))
    return render_template('users/usercreate.html', title=_("Benutzer erstellen - "), form=form, rights=rights)

# USER AVATARS
@bp.route('/avatar/<path:filename>', methods=['GET'])
@login_required
def avatar(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], path=filename)

# GET SOME SPECIFIC ACCESS RIGHTS
def get_user_rights():
    return {
        'create_users': current_user.check_right_or_admin('create_user'),
        'edit_users': current_user.check_right_or_admin('edit_user'),
        'delete_users': current_user.check_right_or_admin('delete_user'),
    }