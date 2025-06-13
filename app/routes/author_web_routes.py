from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.authors_service import AuthorService

web_authors_bp = Blueprint("web_authors_bp", __name__, template_folder="../templates")


@web_authors_bp.route("")
def home():
    return render_template("home.html", title="Welcome to the BookShop")


# --- Author Web Routes ---
@web_authors_bp.route("")
def list_authors():
    authors = AuthorService.get_all_authors()
    return render_template(
        "authors/authors_list.html", authors=authors, title="Authors"
    )


@web_authors_bp.route("/<int:author_id>")
def author_detail(author_id):
    author = AuthorService.get_author_by_id(author_id)
    if not author:
        flash("Author not found.", "error")
        return redirect(url_for("web_authors_bp.list_authors"))
    return render_template(
        "authors/author_detail.html", author=author, title=author.name
    )


@web_authors_bp.route("/new", methods=["GET", "POST"])
def new_author():
    if request.method == "POST":
        name = request.form.get("name")
        bio = request.form.get("bio")
        if not name:
            flash("Author name is required.", "warning")
        else:
            try:
                AuthorService.create_author(name=name, bio=bio)
                flash(f'Author "{name}" created successfully!', "success")
                return redirect(url_for("web_authors_bp.list_authors"))
            except ValueError as e:
                flash(str(e), "error")
    return render_template(
        "authors/author_form.html",
        title="New Author",
        form_action=url_for("web_authors_bp.new_author"),
    )


@web_authors_bp.route("/<int:author_id>/edit", methods=["GET", "POST"])
def edit_author(author_id):
    author = AuthorService.get_author_by_id(author_id)
    if not author:
        flash("Author not found.", "error")
        return redirect(url_for("web_authors_bp.list_authors"))

    if request.method == "POST":
        name = request.form.get("name")
        bio = request.form.get("bio")
        if not name:
            flash("Author name is required.", "warning")
        else:
            try:
                AuthorService.update_author(author_id, name=name, bio=bio)
                flash(f'Author "{name}" updated successfully!', "success")
                return redirect(
                    url_for("web_authors_bp.author_detail", author_id=author_id)
                )
            except ValueError as e:
                flash(str(e), "error")
    return render_template(
        "authors/author_form.html",
        title=f"Edit {author.name}",
        author=author,
        form_action=url_for("web_authors_bp.edit_author", author_id=author_id),
    )


@web_authors_bp.route("/<int:author_id>/delete", methods=["POST"])
def delete_author(author_id):
    author = AuthorService.get_author_by_id(author_id)
    if author:
        try:
            AuthorService.delete_author(author_id)
            flash(
                f'Author "{author.name}" and their books deleted successfully!',
                "success",
            )
        except Exception as e:  # Catch potential DB errors if any
            flash(f"Error deleting author: {str(e)}", "error")
    else:
        flash("Author not found.", "error")
    return redirect(url_for("web_authors_bp.list_authors"))
