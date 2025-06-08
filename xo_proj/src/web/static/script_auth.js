// Скрипт для входа через JWT
function handleLogin(event) {
    event.preventDefault();

    const login = document.querySelector('input[name="login"]').value;
    const password = document.querySelector('input[name="password"]').value;

    fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login, password })
    })
    .then(response => response.json().then(data => ({ status: response.status, data })))
    .then(({ status, data }) => {
        if (status === 200 && data.accessToken && data.refreshToken) {
            // Сохраняем токены
            localStorage.setItem('accessToken', data.accessToken);
            localStorage.setItem('refreshToken', data.refreshToken);
            showPopup('Вход выполнен успешно!', true);
        } else {
            showPopup(data.error || 'Неверный логин или пароль');
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
    document.getElementById("popup").setAttribute("data-success", success);
}

// Закрытие всплывающего окна и переход на главную страницу
function closePopup() {
    const popup = document.getElementById("popup");
    popup.style.display = "none";
    document.getElementById("overlay").style.display = "none";
    if (popup.getAttribute("data-success") === "true") {
        window.location.href = "/";
    }
}
