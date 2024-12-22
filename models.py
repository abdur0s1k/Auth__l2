from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fullname = db.Column(db.String(200))
    nickname = db.Column(db.String(200))
    phone = db.Column(db.String(15))
    gender = db.Column(db.String(10))
    avatar = db.Column(db.String(200))
    date_registered = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
