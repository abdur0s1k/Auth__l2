document.addEventListener("DOMContentLoaded", function () {
    // Тоггл для показа/скрытия пароля
    const togglePasswordButton = document.querySelector('.toggle-password');
    const passwordField = document.getElementById('password');
    
    togglePasswordButton.addEventListener('click', function () {
        if (passwordField.type === "password") {
            passwordField.type = "text";
        } else {
            passwordField.type = "password";
        }
    });

    // Автоввод данных, если пользователь давал согласие
    if (localStorage.getItem('rememberMe') === 'true') {
        const savedLogin = localStorage.getItem('login');
        const savedPassword = localStorage.getItem('password');
        
        if (savedLogin && savedPassword) {
            document.getElementById('login').value = savedLogin;
            document.getElementById('password').value = savedPassword;
            document.getElementById('remember-me').checked = true;
        }
    }

    // Обработчик для кнопки "Войти"
    document.getElementById('login-button').addEventListener('click', function () {
        const login = document.getElementById('login').value;
        const password = document.getElementById('password').value;
        const rememberMe = document.getElementById('remember-me').checked;

        // Валидация данных
        if (!login || !password) {
            showError("Заполните все поля.");
            return;
        }

        // Проверка логина и пароля (эмуляция, в реальном приложении будет запрос к серверу)
        const users = JSON.parse(localStorage.getItem('users')) || [];
        const user = users.find(user => user.login === login);

        if (!user || user.password !== password) {
            showError("Неверно введен логин и/или пароль.");
            return;
        }

        // Если поле "Запомнить меня" отмечено, сохраняем данные
        if (rememberMe) {
            localStorage.setItem('rememberMe', 'true');
            localStorage.setItem('login', login);
            localStorage.setItem('password', password);
        } else {
            localStorage.removeItem('rememberMe');
            localStorage.removeItem('login');
            localStorage.removeItem('password');
        }

        // Успешный вход (переход на другую страницу, например, на главную)
        window.location.href = "home.html"; // Переход на страницу "Главная" или другую
    });

    // Функция для отображения ошибок
    function showError(message) {
        const errorMessage = document.getElementById('error-message');
        errorMessage.textContent = message;
        errorMessage.style.color = "red";
    }
});
