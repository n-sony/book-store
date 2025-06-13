from flask_jwt_extended import create_access_token

from app import db
from app.models.users import ROLE_NAMES, Role, User


class UserService:
    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def create_user(username, email, password, role_name="USER"):
        if UserService.find_by_username(username):
            raise ValueError(f"User with username '{username}' already exists.")
        if UserService.find_by_email(email):
            raise ValueError(f"User with email '{email}' already exists.")

        if role_name not in ROLE_NAMES:
            raise ValueError(f"Role name '{role_name}' not allowed")

        role = Role.query.filter_by(name=role_name).first()

        if not role:
            role = Role(name=role_name)
            db.session.add(role)
            db.session.commit()

        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def update_user(
        user_id,
        email=None,
        username=None,
    ):
        user: User = User.query.get(user_id)
        if not user:
            return None

        if username:
            user.username = username
        if email:
            user.email = email

        db.session.commit()
        return user

    @staticmethod
    def add_role(
        user_id,
        role_name,
    ):
        user: User = User.query.get(user_id)
        if not user:
            return None

        role: Role = Role.query.filter_by(name=role_name)

        user.add_role(role)

        db.session.commit()
        return user

    @staticmethod
    def remove_role(
        user_id,
        role_name,
    ):
        user: User = User.query.get(user_id)
        if not user:
            return None

        role: Role = Role.query.filter_by(name=role_name)

        user.remove_role(role)

        db.session.commit()
        return user

    @staticmethod
    def update_password(
        user_id,
        new_password,
        old_password,
    ):
        user: User = User.query.get(user_id)

        if not user:
            return ValueError("User doesn't exist")

        if new_password == old_password:
            raise ValueError("Old password and new one must be different")

        if User.check_password(old_password):
            raise ValueError("Wrong password")

        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user: User = User.query.get(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True

    @staticmethod
    def login(username, password):
        current_user: User = User.find_by_username(username)
        if not current_user:
            raise ValueError("User not found.")

        if current_user.check_password(password):
            access_token = create_access_token(identity=username)
            return {
                "current_user": current_user.id,
                "access_token": access_token,
                "message": "Login with success",
            }
