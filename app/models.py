from flask import flash, current_app
from flask_babel import _
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin

# -------------------------------------
# Definition of database models
# Models are being mapped to database tables
# -------------------------------------

# User account
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    firstname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    lastname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    email: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, unique=True)
    phone: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    avatar: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    rights: so.Mapped['Right'] = so.relationship(back_populates='user')
    posts: so.Mapped['Post'] = so.relationship(back_populates='user')

    def __repr__(self):
        return '<User {}, id: {}>'.format(self.username, self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_avatar(self, avatar_file):
        filename = secure_filename(avatar_file.filename)
        try:
            avatar_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            self.avatar = filename
        except Exception as e:
            flash(_('Fehler beim Speichern des Bildes: {}').format(e))

    # Check if the user has a specific right
    def check_right(self, right):
        return getattr(self.rights, right)

    # Check if the user is an admin or has a specific right
    def check_right_or_admin(self, right):
        return self.rights.is_admin or self.check_right(right)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

# Rights management
class Right(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    # If a user is an admin, they have all rights except login right (for security purposes)
    is_admin: so.Mapped[bool] = so.mapped_column(default=False)
    # If set to False, a user can't log in, even if admin privileges are granted
    login_allowed: so.Mapped[bool] = so.mapped_column(default=True)
    # Create calendar entries
    create_calendar_entry: so.Mapped[bool] = so.mapped_column(default=False)
    # Create users
    create_user: so.Mapped[bool] = so.mapped_column(default=False)
    # Edit users
    edit_user: so.Mapped[bool] = so.mapped_column(default=False)
    # Delete users
    delete_user: so.Mapped[bool] = so.mapped_column(default=False)
    # Edit rights
    edit_rights: so.Mapped[bool] = so.mapped_column(default=False)

    user: so.Mapped[User] = so.relationship(back_populates='rights')

    def __repr__(self):
        return '<Right by {}, admin: {}, id: >'.format(self.user_id, self.is_admin, self.id)

# Calendar entries
class CalendarEntry(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256))
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    start: so.Mapped[datetime] = so.mapped_column()
    end: so.Mapped[datetime] = so.mapped_column()
    public: so.Mapped[bool] = so.mapped_column(default=False)
    school: so.Mapped[bool] = so.mapped_column(default=False)
    special: so.Mapped[bool] = so.mapped_column(default=False)
    misc: so.Mapped[bool] = so.mapped_column(default=False)

    def __repr__(self):
        return '<CalendarEntry {}, id: {}>'.format(self.title, self.id)

# Message board posts
class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256))
    content: so.Mapped[str] = so.mapped_column(sa.String(1024))
    timestamp: so.Mapped[datetime] = so.mapped_column()
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    answer_to: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('post.id'), index=True)

    user: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}, id: {}>'.format(self.title, self.id)