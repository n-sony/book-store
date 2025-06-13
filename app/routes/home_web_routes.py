from flask import Blueprint, render_template

web_home_bp = Blueprint("web_home_bp", __name__, template_folder="../templates")


@web_home_bp.route("")
def home():
    return render_template("home.html", title="Welcome to the BookShop")
