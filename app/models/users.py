from typing import List

from sqlalchemy.orm import Mapped

from app import db

from ..core import bcrypt

ROLE_NAMES = ["USER", "ADMIN"]


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Role {self.name}>"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    roles: Mapped[List["Role"]] = db.relationship(
        "Role", backref="role", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def add_role(self, new_role: Role):
        for role in self.roles:
            if role.name != new_role.name:
                self.roles.append(new_role)

    def remove_role(self, new_role: Role):
        if len(self.roles) >= 1:
            for role in self.roles:
                if role.name == new_role.name:
                    self.roles.remove(role)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role.name if self.role else None,
        }
