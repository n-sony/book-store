from app import db


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(20), nullable=True, unique=True)
    publication_year = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float, nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "isbn": self.isbn,
            "publication_year": self.publication_year,
            "price": self.price,
            "author_id": self.author_id,
            "author_name": self.author.name if self.author else None,
        }
