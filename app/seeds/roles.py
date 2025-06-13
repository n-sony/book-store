from app import db

from ..models.users import ROLE_NAMES, Role


def seed_roles():
    """Seeds the database with initial user roles."""
    print("Seeding database with initial roles...")

    for role_name in ROLE_NAMES:
        role_exists = Role.query.filter_by(name=role_name).first()
        if not role_exists:
            new_role = Role(name=role_name)
            db.session.add(new_role)
            print(f"Role '{role_name}' created.")
        else:
            print(f"Role '{role_name}' already exists.")

    db.session.commit()
    db.session.commit()
