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

    // Регистрация (например, просто выводим сообщение)
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

        // Здесь можно добавить код для отправки данных на сервер
        alert(`Регистрация успешна для ${name} (${nickname})!`);
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
