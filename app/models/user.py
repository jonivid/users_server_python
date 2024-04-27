from app import db
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import DateTime
from sqlalchemy.sql import func

ph = PasswordHasher()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)  # Adjusted length for Argon2 hash
    first_name = db.Column(db.String(100),nullable=True)
    last_name = db.Column(db.String(100),nullable=True)
    role= db.Column(db.String(80),default="user") 
    is_active = db.Column(db.Boolean, default=True)
    date_created = db.Column(DateTime(timezone=True), server_default=func.now())
    date_modified = db.Column(DateTime(timezone=True), onupdate=func.now())


    def set_password(self, password):
        self.password_hash = ph.hash(password)

    def check_password(self, password):
        try:
            return ph.verify(self.password_hash, password)
        except VerifyMismatchError:
            return False
