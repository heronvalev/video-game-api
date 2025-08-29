from flask import Blueprint, render_template, request, flash, session
from datetime import datetime, timedelta
from flask_login import current_user
from app.auth import generate_token

# Blueprint for home page
main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def home():

    token = None
    token_expired = True

    # Check if a token exists in the session
    stored_token = session.get("api_token")
    token_expiration = session.get("api_token_expiration")

    if stored_token and token_expiration:
        # Convert string back to datetime
        token_expiration_dt = datetime.fromisoformat(token_expiration)
        if datetime.utcnow() < token_expiration_dt:
            token = stored_token
            token_expired = False

    # Only generate new token if user is logged in and token expired
    if request.method == "POST" and current_user.is_authenticated and token_expired:
        token = generate_token(current_user.id)
        flash("Your token has been generated. Copy it below.", "success")
        
        # Store token and expiration in session
        session["api_token"] = token
        session["api_token_expiration"] = (datetime.utcnow() + timedelta(hours=1)).isoformat()

    return render_template(
        "index.html",
        current_year=datetime.now().year,
        token=token,
        token_expired=token_expired,
        current_user=current_user
    )

@main_bp.route("/about")
def about():
    return render_template("about.html", current_year=datetime.now().year)