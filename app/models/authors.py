from app import db


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    bio = db.Column(db.Text, nullable=True)

    books = db.relationship(
        "Book", backref="author", lazy=True, cascade="all, delete-orphan"
    )

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"<Author {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
            "book_ids": [book.id for book in self.books],
        }
