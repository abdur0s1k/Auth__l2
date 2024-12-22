document.addEventListener("DOMContentLoaded", function () {
    // Тоггл для показа/скрытия паролей
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function () {
            const targetId = button.getAttribute('data-target');
            const targetInput = document.getElementById(targetId);
            if (targetInput.type === "password") {
                targetInput.type = "text";
            } else {
                targetInput.type = "password";
            }
        });
    });

    // Генерация случайного пароля
    document.getElementById('generate-password').addEventListener('click', function () {
        const password = generatePassword();
        document.getElementById('password').value = password;
        document.getElementById('confirm-password').value = password;
    });

    // Регистрация (отправка данных на сервер)
    document.getElementById('register-button').addEventListener('click', function () {
        const name = document.getElementById('name').value;
        const nickname = document.getElementById('nickname').value;
        const phone = document.getElementById('phone').value;
        const gender = document.getElementById('gender').value;
        const login = document.getElementById('login').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (password !== confirmPassword) {
            alert("Пароли не совпадают!");
            return;
        }

        // Валидация данных
        if (!name || !nickname || !phone || !gender || !login || !password) {
            alert("Заполните все поля.");
            return;
        }

        // Отправка данных на сервер
        const userData = {
            name: name,
            nickname: nickname,
            phone: phone,
            gender: gender,
            login: login,
            password: password
        };

        fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Регистрация успешна!");
                window.location.href = 'login.html'; // Перенаправление на страницу входа
            } else {
                alert(data.message || "Произошла ошибка при регистрации.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Произошла ошибка при отправке данных на сервер.");
        });
    });

    // Функция генерации случайного пароля
    function generatePassword() {
        const charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()";
        let password = "";
        for (let i = 0; i < 12; i++) {
            const randomIndex = Math.floor(Math.random() * charset.length);
            password += charset[randomIndex];
        }
        return password;
    }
});
