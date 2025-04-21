const body = document.body;
const currentUserLogin = body.dataset.userLogin;
let gameEnded = false;

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("symbolSelection").style.display = "block";
});

async function startMultiGame() {
    gameEnded = false;
    const playerSymbolElement = document.querySelector('input[name="player_symbol"]:checked');
    const playerSymbol = playerSymbolElement.value;

    // Скрываем выбор символа и показываем экран ожидания
    document.getElementById("symbolSelection").style.display = "none";
    document.getElementById("waitingScreen").style.display = "block";

    const response = await fetch("/new_multi_game", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({player_symbol: playerSymbol})
    });

    const data = await response.json();

    if (data && data.game_id) {
        // Показываем ID игры для подключения
        document.getElementById("gameIdDisplay").textContent = data.game_id;

        // Начинаем проверять статус игры каждые 5 секунд
        const checkInterval = setInterval(async () => {
            const statusResponse = await fetch(`/game/${data.game_id}`);
            const statusData = await statusResponse.json();

            console.log("Game status check:", statusData);

            if (statusData.user2_id) {
                // Второй игрок подключился
                clearInterval(checkInterval);
                document.getElementById("waitingScreen").style.display = "none";

                // Показываем информацию о сопернике
                document.getElementById("opponentInfo").textContent =
                    `Соперник: ${statusData.player2_user_login} (${statusData.player2_symbol})`;

                // Загружаем игру
                await loadGame(data.game_id);
            }
        }, 5000);
    } else {
        console.error("Ошибка при создании игры, сервер недоступен");
        document.getElementById("symbolSelection").style.display = "block";
        document.getElementById("waitingScreen").style.display = "none";
    }
}

// Функция для копирования ID игры
function copyGameId() {
    const gameId = document.getElementById("gameIdDisplay").textContent;
    navigator.clipboard.writeText(gameId).then(() => {
        alert("ID игры скопирован в буфер обмена!");
    }).catch(err => {
        console.error("Не удалось скопировать ID: ", err);
    });
}

async function beginMultiGame(game_id) {
    document.getElementById("symbolSelection").style.display = "none";
    await loadGame(game_id);
}

async function loadGame(gameId) {
    if (!gameId) return;
    const response = await fetch(`/game/${gameId}`);
    const data = await response.json();
    renderBoard(gameId, data);
}


async function makeMove(gameId, row, col) {
    await fetch(`/game_multi/${gameId}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({row, col})
    });
    await loadGame(gameId);  // Обновляем игровое поле после хода

}

function renderBoard(gameId, data) {
    const [status, userLogin] = data.statement.split(" ");
    const isCurrentPlayersTurn = currentUserLogin === userLogin;
    if (data.is_game_over && !gameEnded) {
        showEndScreen(userLogin, status);
    }

    const table = document.getElementById("gameBoard");
    table.innerHTML = "";  // Очищаем старое поле
    data.board.forEach((row, i) => {
        const tr = document.createElement("tr");
        row.forEach((cell, j) => {
            const td = document.createElement("td");
            td.style.transition = "opacity 0.3s, cursor 0.3s";  // анимация
            if (cell === 1) {
                td.textContent = "X";
                td.style.color = "#FF5733";
            } else if (cell === 2) {
                td.textContent = "O";
                td.style.color = "#3498DB";
            } else {
                td.textContent = "";
            }
            if (!data.is_game_over) {
                if (isCurrentPlayersTurn) {
                    td.onclick = () => makeMove(gameId, i, j);
                    td.style.cursor = "pointer";
                    td.style.opacity = "1";
                } else {
                    td.onclick = null;
                    td.style.cursor = "not-allowed";
                    td.style.opacity = "0.6";
                }
            }

            tr.appendChild(td);
        });
        table.appendChild(tr);
    });
    // Если игра не закончилась — повторно вызвать renderBoard через 5 сек
    if (!data.is_game_over) {
        boardUpdateTimeout = setTimeout(async () => {
            try {
                const response = await fetch(`/game/${gameId}`);
                const newData = await response.json();
                renderBoard(gameId, newData);  // рекурсивный вызов
            } catch (err) {
                console.error("Ошибка при обновлении статуса игры:", err);
            }
        }, 2000);
    }
    showInfoScreen(data, status, userLogin, isCurrentPlayersTurn);
}

function showInfoScreen(data, status, userLogin, isCurrentPlayersTurn) {
    // Корректное отображение текущего игрока
    if (data.user_login === currentUserLogin) {
        document.getElementById("playerDisplay").innerHTML =
            `Вы игрок ${data.user_login} играете за: ${data.player_symbol}
            <br><br>Соперник: ${data.user2_login} играет ${data.player2_symbol}`;
    } else {
        document.getElementById("playerDisplay").innerHTML =
            `Вы игрок ${data.user2_login} играете за: ${data.player2_symbol}
             <br><br>Соперник: ${data.user_login} играет за: ${data.player_symbol}`;
    }

    if (status !== "win_player" && status !== "draw") {
        const statementText = isCurrentPlayersTurn
            ? "Ваш ход!"
            : `Ожидаем ход игрока: ${userLogin}`;
        document.getElementById("statement").textContent =
            `Текущее состояние игры: ${statementText}`;
    } else if (status === "draw") {
        document.getElementById("statement").textContent = "Игра окончена: ничья!";
    } else {
        document.getElementById("statement").textContent =
            `Игра окончена: победил игрок ${userLogin}`;
    }

    document.getElementById("game_id").textContent =
        `ID игры: ${data.game_id}`;
}

function showEndScreen(userLogin, status) {
    setTimeout(() => {
        gameEnded = true;
        disableBoard();
        let message;
        let icon;
        if (userLogin === currentUserLogin) {
            message = "Вы победили!";
            icon = "success";
        }
        if (userLogin !== currentUserLogin) {
            message = "Вы проиграли";
            icon = "error";
        }
        if (status === "draw") {
            message = "Ничья!";
            icon = "warning";
        }
        Swal.fire({
            title: "Игра окончена!",
            text: message,
            icon: icon,
            confirmButtonText: "OK",
        });
    }, 10); // Даем небольшую задержку для отображения доски
}

function disableBoard() {
    const cells = document.querySelectorAll("#gameBoard td");
    cells.forEach(cell => {
        cell.onclick = null; // Убираем обработчики кликов
        cell.style.cursor = "not-allowed"; // Меняем курсор на "недоступно"
    });
}


