from flask import Flask, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

# Модель пользователя
class User(db.Model):
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
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Генерация случайного пароля
def generate_random_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# Авторизация и регистрация
@app.route('/auth/register', methods=['POST'])
def register():
    login = request.form['login']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    # Проверка на пробелы в логине и пароле
    if " " in login or " " in password or " " in confirm_password:
        return jsonify({"success": False, "message": "Логин и пароль не могут содержать пробелы."}), 400
    
    # Проверка совпадения паролей
    if password != confirm_password:
        return jsonify({"success": False, "message": "Пароли не совпадают."}), 400

    user = User.query.filter_by(login=login).first()
    if user:
        return jsonify({"success": False, "message": "Пользователь с таким логином уже существует."}), 400

    # Генерация случайного пароля если не введен
    if not password:
        password = generate_random_password()

    new_user = User(login=login, email=request.form.get('email'), name=request.form.get('name'), 
                    nickname=request.form.get('nickname'), phone=request.form.get('phone'), 
                    gender=request.form.get('gender'), avatar=request.form.get('avatar'))
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    flash('Аккаунт создан', 'success')
    return jsonify({"success": True, "message": "Аккаунт создан успешно."})

@app.route('/auth/login', methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']
    
    user = User.query.filter_by(login=login).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"success": True, "message": "Вход выполнен успешно!"})
    
    return jsonify({"success": False, "message": "Неверный логин или пароль."}), 401

@app.route('/auth/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"success": True, "message": "Выход выполнен успешно!"})

# Личный кабинет
@app.route('/user/profile', methods=['GET'])
@login_required
def profile():
    return jsonify({
        "login": current_user.login,
        "name": current_user.name,
        "nickname": current_user.nickname,
        "phone": current_user.phone,
        "gender": current_user.gender,
        "avatar": current_user.avatar,
        "email": current_user.email,
        "registration_date": current_user.registration_date
    })

@app.route('/user/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    current_user.name = request.form.get('name', current_user.name)
    current_user.nickname = request.form.get('nickname', current_user.nickname)
    current_user.phone = request.form.get('phone', current_user.phone)
    current_user.gender = request.form.get('gender', current_user.gender)
    current_user.avatar = request.form.get('avatar', current_user.avatar)
    db.session.commit()
    return jsonify({"success": True, "message": "Данные обновлены."})

# Инициализация базы данных
@app.before_first_request
def init_db():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
