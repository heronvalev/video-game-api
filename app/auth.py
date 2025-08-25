from flask import Blueprint, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime
from . import db
from .models import User

# Blueprint for user authentication routes (login/register)
auth_bp = Blueprint("auth", __name__)

# WTForms classes for user registration and login
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Log In")

# Register route
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        # Check if user email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email is already registered. Please log in.", "danger")
            return redirect(url_for("auth.login"))
        
        # Create new user
        new_user = User(name=form.name.data, email=form.email.data)
        new_user.set_password(form.password.data)

        # Add to database and commit
        db.session.add(new_user)
        db.session.commit()

        # Success message and redirect to login
        flash("Registration successful! Please log in.", "success")

        return redirect(url_for("auth.login"))
    
    return render_template("register.html", current_year = datetime.now().year, form=form)

# Log in route
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", current_year = datetime.now().year)