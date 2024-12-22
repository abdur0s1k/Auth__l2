from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Product, User
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Не забывайте изменить ключ на более безопасный

db.init_app(app)

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('register.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        fullname = request.form['fullname']
        nickname = request.form.get('nickname')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        avatar = request.files.get('avatar')
        email = request.form['email']  # Добавлено поле для email

        # Проверка совпадения паролей
        if password != confirm_password:
            flash("Пароли не совпадают!", "danger")
            return redirect(url_for('register'))

        # Хешируем пароль
        hashed_password = generate_password_hash(password)

        # Создаем нового пользователя
        new_user = User(username=username, password=hashed_password, email=email, fullname=fullname,
                        nickname=nickname, phone=phone, gender=gender, avatar=avatar.filename)

        db.session.add(new_user)
        db.session.commit()

        flash("Вы успешно зарегистрированы! Теперь вы можете войти.", "success")
        return redirect(url_for('login'))  # Перенаправление на страницу входа

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Вы успешно вошли!", "success")
            return redirect(url_for('profile'))
        else:
            flash("Неверный логин или пароль", "danger")
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash("Пожалуйста, войдите в аккаунт", "danger")
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Удаляем информацию о пользователе из сессии
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))  # Перенаправление на страницу входа


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Product.query.first():
            sample_products = [
                Product(name="JoyStick ONE", price=919.99, category="PC", image_url="images/product-1.png"),
                Product(name="JoyStick FURY", price=1249.99, category="PC", image_url="images/product-2.png"),
            ]
            db.session.add_all(sample_products)
            db.session.commit()
    app.run(debug=True)
