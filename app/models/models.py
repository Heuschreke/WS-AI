from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    looks: so.Mapped["Look"] = so.relationship(back_populates="user")

    def __repr__(self):
        return "<User {}>".format(self.username)


class Look(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    name: so.Mapped[str] = so.mapped_column(sa.String(100))

    image_url: so.Mapped[str] = so.mapped_column(sa.String(200))

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    user: so.Mapped[User] = so.relationship(back_populates="looks")

    def __repr__(self):
        return "<Look {}>".format(self.image_url)
