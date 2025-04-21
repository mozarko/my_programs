// Скрипт для отправки данных с использованием Basic Auth
function handleLogin(event) {
    event.preventDefault(); // Отменяем стандартную отправку формы
    const login = document.querySelector('input[name="login"]').value;
    const password = document.querySelector('input[name="password"]').value;
    // Создаем строку "login:password"
    const credentials = btoa(login + ':' + password);
    // Создаем заголовок Authorization
    const headers = {
        'Authorization': 'Basic ' + credentials
    };
    // Выполняем запрос с заголовками
    fetch('/login', {
        method: 'POST',
        headers: headers
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showPopup('Неверный логин или пароль'); // Показываем ошибку если есть
        } else {
            showPopup('Вход выполнен успешно!', true);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        showPopup(error.message);
        });
    }

    // Показ всплывающего окна
    function showPopup(message, success = false) {
        document.getElementById("popup-message").innerText = message;
        document.getElementById("popup").style.display = "block";
        document.getElementById("overlay").style.display = "block";
        // Запоминаем, нужно ли сделать редирект после закрытия
        document.getElementById("popup").setAttribute("data-success", success);
    }

    // Закрытие всплывающего окна и переход на главную страницу
    function closePopup() {
        const popup = document.getElementById("popup");
        const overlay = document.getElementById("overlay");
        popup.style.display = "none";
        overlay.style.display = "none";
        // Если вход успешен, перенаправляем на главную страницу
        if (popup.getAttribute("data-success") === "true") {
            window.location.href = "/";
    }
}