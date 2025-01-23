from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash

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

    rights: so.Mapped['Right'] = so.relationship(back_populates='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

# Rights management
class Right(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    is_admin: so.Mapped[bool] = so.mapped_column(default=False)
    login_allowed: so.Mapped[bool] = so.mapped_column(default=True)
    create_calendar_entry: so.Mapped[bool] = so.mapped_column(default=False)

    user: so.Mapped[User] = so.relationship(back_populates='rights')

    def __repr__(self):
        return '<Right by {}, admin: {}>'.format(self.user_id, self.is_admin)