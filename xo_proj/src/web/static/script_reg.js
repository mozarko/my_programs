// Функция для показа всплывающего окна
function showPopup(message, redirectUrl) {
    const popupMessage = document.getElementById("popup-message");
    popupMessage.textContent = message;
    document.getElementById("popup").style.display = "block";
    document.getElementById("overlay").style.display = "block";

    // Закрытие всплывающего окна
    document.querySelector("#popup button").onclick = function () {
        closePopup(redirectUrl);
    };
}

// Закрытие всплывающего окна
function closePopup(redirectUrl) {
    document.getElementById("popup").style.display = "none";
    document.getElementById("overlay").style.display = "none";
    if (redirectUrl) {
        window.location.href = redirectUrl;
    }
}

// Обработка отправки формы регистрации через fetch
document.getElementById("registerForm").onsubmit = async function(e) {
    e.preventDefault();
    let login = this.login.value;
    let password = this.password.value;
    let response = await fetch('/auth/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({login, password})
    });
    let data = await response.json();
    if (response.status === 201) {
        showPopup('Регистрация успешна!', '/login');
    } else if (response.status === 409) {
        showPopup('Ошибка регистрации: пользователь уже существует!', null);
    } else {
        showPopup(data.error || 'Ошибка регистрации', null);
    }
};