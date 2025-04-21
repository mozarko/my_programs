document.addEventListener("DOMContentLoaded", () => {
        document.getElementById("symbolSelection").style.display = "block";
});

async function startNewGame() {
    const playerSymbolElement = document.querySelector('input[name="player_symbol"]:checked');

    playerSymbol = playerSymbolElement.value;
    document.getElementById("playerSymbolDisplay").style.display = "block";
    document.getElementById("newGameButton").style.display = "block";

    const response = await fetch("/new_game", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({player_symbol: playerSymbol})
    });

    const data = await response.json();

    if (data) {
        document.getElementById("symbolSelection").style.display = "none"; //
        await loadGame(data.game_id);
    } else {
        console.error("Ошибка при создании игры, сервер недоступен");
    }
}

async function startMultiGame() {
    const playerSymbolElement = document.querySelector('input[name="player_symbol"]:checked');

    playerSymbol = playerSymbolElement.value;
    document.getElementById("playerSymbolDisplay").style.display = "block";
    document.getElementById("newGameButton").style.display = "block";

    const response = await fetch("/new_multi_game", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({player_symbol: playerSymbol})
    });

    const data = await response.json();

    if (data) {
        document.getElementById("symbolSelection").style.display = "none"; //
        await loadGame(data.game_id);
    } else {
        console.error("Ошибка при создании игры, сервер недоступен");
    }
}

async function continueGame(game_id) {
    document.getElementById("symbolSelection").style.display = "none";
    await loadGame(game_id);
}

async function loadGame(gameId) {
    if (!gameId) return;
    const response = await fetch(`/game/${gameId}`);
    const data = await response.json();
    renderBoard(gameId, data.board, data.player_symbol, data.is_game_over, data.computer_first_move);
}

async function make_first_computer_move(gameId) {
    await fetch(`/game/${gameId}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify("computer_first_move")
    });

    await loadGame(gameId);  // Обновляем игровое поле после хода
}


async function makeMove(gameId, row, col) {

    const response = await fetch(`/game/${gameId}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({row, col})
    });

    const data = await response.json();
    await loadGame(gameId);  // Обновляем игровое поле после хода

    setTimeout(() => {
        if (data.is_game_over) {
//            isGameOver = true;
            let message;
            let icon;
            if (data.winner === "player") {
                message = "Вы победили!";
                icon = "success";
            }
            if (data.winner === "computer") {
                message = "Компьютер победил!";
                icon = "error";
            }
            if (data.winner === "draw") {
                message = "Ничья!";
                icon = "warning";
            }
            Swal.fire({
                title: "Игра окончена!",
                text: message,
                icon: icon,
                confirmButtonText: "OK",
            });
            // Скрываем "Вы играете за:"
            document.getElementById("playerSymbolDisplay").style.display = "none";
            // Показываем кнопку "Начать новую игру"
            document.getElementById("newGameButton").style.display = "block";
            // Выключаем возможность взаимодействия с доской
            disableBoard();
        }
    }, 10); // Даем небольшую задержку для отображения доски
}

function renderBoard(gameId, board, playerSymbol, isGameOver, computer_first_move) {
    const table = document.getElementById("gameBoard");
    table.innerHTML = "";  // Очищаем старое поле

    if (computer_first_move) {
        make_first_computer_move(gameId);
    }

    board.forEach((row, i) => {
        const tr = document.createElement("tr");
        row.forEach((cell, j) => {
            const td = document.createElement("td");
            if (cell === 1) {
                td.textContent = "X";
                td.style.color = "#FF5733";
            } else if (cell === 2) {
                td.textContent = "O";
                td.style.color = "#3498DB";
            } else {
                td.textContent = "";
            }
            if (!isGameOver) {
                td.onclick = () => makeMove(gameId, i, j);
            }
            tr.appendChild(td);
        });
        table.appendChild(tr);
    });

    // Корректное отображение текущего игрока
    document.getElementById("playerSymbolDisplay").textContent =
        `Вы играете за: ${playerSymbol}`;
        document.getElementById("newGameButton").style.display = "block";
}

function disableBoard() {
    const cells = document.querySelectorAll("#gameBoard td");
    cells.forEach(cell => {
        cell.onclick = null; // Убираем обработчики кликов
        cell.style.cursor = "not-allowed"; // Меняем курсор на "недоступно"
    });
}


