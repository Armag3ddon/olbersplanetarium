from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    firstname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    lastname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    email: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, unique=True)
    phone: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)