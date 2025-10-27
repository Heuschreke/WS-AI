from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    looks: so.Mapped[list["Look"]] = so.relationship(back_populates="user")

    is_admin: so.Mapped[bool] = so.mapped_column(default=False)

    def __repr__(self):
        return "<User {}>".format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Look(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    name: so.Mapped[str] = so.mapped_column(sa.String(100))

    image_url: so.Mapped[str] = so.mapped_column(sa.String(200))

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)

    user: so.Mapped["User"] = so.relationship(back_populates="looks")

    def __repr__(self):
        return "<Look {}>".format(self.image_url)
    
class Category(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    subcategories: so.Mapped[list["SubCategory"]] = so.relationship(back_populates="category")

class SubCategory(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("category.id"), index=True)
    category: so.Mapped["Category"] = so.relationship(back_populates="subcategories")
    garments: so.Mapped[list["Garment"]] = so.relationship(back_populates="subcategory")


class Garment(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    price: so.Mapped[int] = so.mapped_column(sa.Integer)
    brand: so.Mapped[str] = so.mapped_column(sa.String(64))
    size: so.Mapped[str] = so.mapped_column(sa.String(64))
    color: so.Mapped[str] = so.mapped_column(sa.String(64))
    gender: so.Mapped[str] = so.mapped_column(sa.String(64))
    image_url: so.Mapped[str] = so.mapped_column(sa.String(200))
    marketplace_id: so.Mapped[int] = so.mapped_column(sa.Integer)
    subcategory_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("sub_category.id"), index=True)
    subcategory: so.Mapped["SubCategory"] = so.relationship(back_populates="garments")
