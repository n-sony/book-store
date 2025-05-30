from app import db
from app.models.authors import Author


class AuthorService:
    @staticmethod
    def get_all_authors():
        return Author.query.all()

    @staticmethod
    def get_author_by_id(author_id):
        return Author.query.get(author_id)

    @staticmethod
    def create_author(name, bio=None):
        if Author.query.filter_by(name=name).first():
            raise ValueError(f"Author with name '{name}' already exists.")
        new_author = Author(name=name, bio=bio)
        db.session.add(new_author)
        db.session.commit()
        return new_author

    @staticmethod
    def update_author(author_id, name=None, bio=None):
        author = Author.query.get(author_id)
        if not author:
            return None
        if name:
            # Check if another author with the new name already exists
            existing_author = Author.query.filter(
                Author.name == name, Author.id != author_id
            ).first()
            if existing_author:
                raise ValueError(f"Another author with name '{name}' already exists.")
            author.name = name
        if bio is not None:  # Allow clearing bio
            author.bio = bio
        db.session.commit()
        return author

    @staticmethod
    def delete_author(author_id):
        author = Author.query.get(author_id)
        if not author:
            return False
        db.session.delete(author)
        db.session.commit()
        return True
