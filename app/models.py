from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    """Load user by their ID"""
    return User.query.get(int(id))



class User(db.Model, UserMixin):
    """User table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'User: {self.username}'

    def set_password(self, password):
        """Hash user password befor storage"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Confirms a user's password"""
        return check_password_hash(self.password_hash, password)
