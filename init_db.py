from run import app
from app import db

with app.app_context():
    db.create_all()
    print("Database tables created.")