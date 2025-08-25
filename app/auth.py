from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# Blueprint for user authentication routes (login/register)
auth_bp = Blueprint("auth", __name__)

# Register route
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

# Log in route
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")