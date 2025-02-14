from app import db
import re
from sqlalchemy.orm import validates

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @validates("email")
    def validate_email(self, key, email):
        if not re.match(r"^[\w\.-]+@([\w\-]+\.)+[a-zA-Z]{2,4}$", email):
            raise ValueError("Invalid email format")
        return email