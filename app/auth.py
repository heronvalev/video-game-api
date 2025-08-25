from flask import Blueprint
from flask_wtf
# Blueprint for user authentication routes (login/register)
auth_bp = Blueprint("auth", __name__)

# Register route
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    pass