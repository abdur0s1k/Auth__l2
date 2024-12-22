from flask import Flask, request, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import string
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/path/to/your/database/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db_dir = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'][10:])
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

login_manager = LoginManager(app)
login_manager.login_view = "login"  # Обеспечивает редирект на страницу входа, если не авторизован

# Функция user_loader для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))  # Перенаправить на личный кабинет, если пользователь авторизован
    return redirect(url_for('login'))  # Перенаправить на страницу логина, если пользователь не авторизован

# Регистрация
@app.route('/auth/register', methods=['POST'])
def register():
    login = request.form['login']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    email = request.form.get('email')
    
    # Проверка на пробелы в логине и пароле
    if " " in login or " " in password or " " in confirm_password:
        return jsonify({"success": False, "message": "Логин и пароль не могут содержать пробелы."}), 400
    
    # Проверка совпадения паролей
    if password != confirm_password:
        return jsonify({"success": False, "message": "Пароли не совпадают."}), 400

    # Проверка уникальности логина и email
    if User.query.filter_by(login=login).first():
        return jsonify({"success": False, "message": "Пользователь с таким логином уже существует."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Пользователь с таким email уже существует."}), 400

    # Генерация случайного пароля если не введен
    if not password:
        password = generate_random_password()

    new_user = User(login=login, email=email, name=request.form.get('name'), 
                    nickname=request.form.get('nickname'), phone=request.form.get('phone'), 
                    gender=request.form.get('gender'), avatar=request.form.get('avatar'))
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    flash('Аккаунт создан', 'success')
    return jsonify({"success": True, "message": "Аккаунт создан успешно."})

# Вход
@app.route('/auth/login', methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']
    
    user = User.query.filter_by(login=login).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"success": True, "message": "Вход выполнен успешно!"})
    
    return jsonify({"success": False, "message": "Неверный логин или пароль."}), 401

# Выход
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

# Редактирование профиля
@app.route('/user/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    name = request.form.get('name')
    nickname = request.form.get('nickname')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    avatar = request.form.get('avatar')

    if name:
        current_user.name = name
    if nickname:
        current_user.nickname = nickname
    if phone:
        current_user.phone = phone
    if gender:
        current_user.gender = gender
    if avatar:
        current_user.avatar = avatar

    db.session.commit()
    return jsonify({"success": True, "message": "Данные обновлены."})

# Инициализация базы данных
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Инициализация базы данных
    app.run(debug=True)
