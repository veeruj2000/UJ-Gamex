document.addEventListener("DOMContentLoaded", () => {
    const cells = document.querySelectorAll(".cell");
    const statusDisplay = document.getElementById("status");
    const resetButton = document.getElementById("reset");
    const scoreDisplay = document.getElementById("score");
    let board = ["", "", "", "", "", "", "", "", ""];
    let currentPlayer = "X";
    let gameActive = true;

    const winningConditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
        [0, 4, 8], [2, 4, 6]             // Diagonals
    ];

    function checkWinner() {
        for (let condition of winningConditions) {
            let [a, b, c] = condition;
            if (board[a] && board[a] === board[b] && board[a] === board[c]) {
                gameActive = false;
                statusDisplay.innerText = `Player ${board[a]} Wins! 🎉`;
                updateScore(board[a] === "X" ? "win" : "loss");
                return;
            }
        }

        if (!board.includes("")) {
            gameActive = false;
            statusDisplay.innerText = "It's a Draw! 🤝";
            updateScore("draw");
        }
    }

    function handleCellClick(event) {
        const cellIndex = event.target.id;
        if (board[cellIndex] !== "" || !gameActive) return;

        board[cellIndex] = currentPlayer;
        event.target.innerText = currentPlayer;
        checkWinner();

        currentPlayer = currentPlayer === "X" ? "O" : "X";
        statusDisplay.innerText = `Player ${currentPlayer}'s Turn`;
    }

    function resetGame() {
        board = ["", "", "", "", "", "", "", "", ""];
        gameActive = true;
        currentPlayer = "X";
        statusDisplay.innerText = "Player X's Turn";
        cells.forEach(cell => cell.innerText = "");
    }

    function updateScore(result) {
        fetch("/update-score/", {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `result=${result}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                scoreDisplay.innerText = `Wins: ${data.wins}, Losses: ${data.losses}, Draws: ${data.draws}`;
            }
        })
        .catch(error => console.error("Error updating score:", error));
    }

    cells.forEach(cell => cell.addEventListener("click", handleCellClick));
    resetButton.addEventListener("click", resetGame);
});
