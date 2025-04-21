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