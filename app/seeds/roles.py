def seed_roles(user, db):
    if not user.Role.query.filter_by(name="admin").first():
        db.session.add(user.Role(name="admin"))
    if not user.Role.query.filter_by(name="user").first():
        db.session.add(user.Role(name="user"))
    db.session.commit()
