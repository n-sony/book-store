from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.services.users_service import UserService

web_auth_bp = Blueprint("web_auth_bp", __name__, template_folder="../templates")


@web_auth_bp.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = UserService.find_by_id(user_id) if user_id is not None else None


@web_auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if g.user:
        return redirect(url_for("web_home_bp.home"))
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        try:
            UserService.create_user(username, email, password)
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("web_auth_bp.login"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("auth/register.html", title="Register")


@web_auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if g.user:
        return redirect(url_for("web_home_bp.home"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = UserService.find_by_username(username)
        if user and user.check_password(password):
            session.clear()
            session["user_id"] = user.id
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for("web_home_bp.home"))
        else:
            flash("Invalid username or password.", "error")
    return render_template("auth/login.html", title="Login")


@web_auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("web_auth_bp.login"))
