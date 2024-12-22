from datetime import datetime
from backend.app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=True)
    nickname = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    avatar = db.Column(db.String(120), nullable=True)  # Ссылка на аватар
    email = db.Column(db.String(120), unique=True, nullable=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        from backend.utils.hash import hash_password
        self.password = hash_password(password)

    def check_password(self, password):
        from backend.utils.hash import check_password
        return check_password(self.password, password)
