from flask_jwt_extended import create_access_token

from app import db
from app.models.users import User


class UserService:
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def create_user(username, role, password):
        if username and User.query.filter_by(username=username).first():
            raise ValueError("User with username already exist")

        new_user = User(
            username=username,
            password=User.generate_hash(password),
            role=role,
        )

        return new_user.create()

    @staticmethod
    def update_user(
        user_id,
        username=None,
        role=None,
    ):
        user = User.query.get(user_id)
        if not user:
            return None

        if username:
            user.username = username
        if role:
            user.role = role

        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True

    @staticmethod
    def login(username, password):
        current_user = User.find_by_username(username)
        if not current_user:
            raise ValueError("User not found.")

        if User.verify_hash(password, current_user.password):
            access_token = create_access_token(identity=username)
            return {"access_token": access_token, "message": "Login with success"}
