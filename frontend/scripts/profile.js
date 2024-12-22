document.addEventListener("DOMContentLoaded", function () {
    // Загрузка данных пользователя из localStorage
    const user = JSON.parse(localStorage.getItem('currentUser'));
    
    if (!user) {
        alert("Вы не авторизованы!");
        window.location.href = "login.html"; // Перенаправляем на страницу входа
        return;
    }

    // Отображение данных пользователя
    document.getElementById('user-login').textContent = user.login;
    document.getElementById('user-nickname').textContent = user.nickname;
    document.getElementById('user-email').textContent = user.email;
    document.getElementById('user-registration-date').textContent = user.registrationDate;

    // Обработчик кнопки выхода
    document.getElementById('logout-button').addEventListener('click', function () {
        localStorage.removeItem('currentUser');
        window.location.href = "login.html"; // Перенаправляем на страницу входа
    });

    // Обработчик кнопки редактирования профиля
    document.getElementById('edit-profile-button').addEventListener('click', function () {
        document.querySelector('.edit-form').style.display = 'block';
        document.getElementById('new-nickname').value = user.nickname;
        document.getElementById('new-email').value = user.email;
        // Не показываем старый пароль
    });

    // Обработчик сохранения изменений
    document.getElementById('save-changes-button').addEventListener('click', function () {
        const newNickname = document.getElementById('new-nickname').value;
        const newEmail = document.getElementById('new-email').value;
        const newPassword = document.getElementById('new-password').value;

        // Валидация данных
        if (!newNickname || !newEmail || !newPassword) {
            alert("Пожалуйста, заполните все поля!");
            return;
        }

        // Обновление данных в объекте пользователя
        user.nickname = newNickname;
        user.email = newEmail;
        user.password = newPassword;

        // Сохранение обновленных данных в localStorage
        localStorage.setItem('currentUser', JSON.stringify(user));

        // Обновление информации на странице
        document.getElementById('user-nickname').textContent = newNickname;
        document.getElementById('user-email').textContent = newEmail;

        // Скрытие формы редактирования
        document.querySelector('.edit-form').style.display = 'none';
        alert("Изменения сохранены.");
    });

    // Обработчик отмены изменений
    document.getElementById('cancel-changes-button').addEventListener('click', function () {
        document.querySelector('.edit-form').style.display = 'none';
    });
});
