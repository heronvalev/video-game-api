from flask import Blueprint, render_template
from datetime import datetime

# Blueprint for home page
main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("index.html", current_year = datetime.now().year)
