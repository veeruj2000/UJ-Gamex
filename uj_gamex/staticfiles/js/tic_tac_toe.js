document.addEventListener("DOMContentLoaded", function () {
    let board = ["", "", "", "", "", "", "", "", ""];
    let currentPlayer = "X"; // User is X, AI is O
    let gameActive = true;

    const cells = document.querySelectorAll(".cell");
    const statusDisplay = document.getElementById("status");
    const resetButton = document.getElementById("reset");
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    function checkWinner(board) {
        const winningCombinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], 
            [0, 3, 6], [1, 4, 7], [2, 5, 8], 
            [0, 4, 8], [2, 4, 6]
        ];
        for (let combo of winningCombinations) {
            let [a, b, c] = combo;
            if (board[a] && board[a] === board[b] && board[a] === board[c]) {
                return board[a]; // "X" or "O" wins
            }
        }
        return board.includes("") ? null : "draw"; // "draw" if no moves left
    }

    function aiMove() {
        if (!gameActive) return;

        let emptyCells = board
            .map((val, idx) => (val === "" ? idx : null))
            .filter(val => val !== null);

        if (emptyCells.length === 0) return;

        let bestMove = emptyCells[Math.floor(Math.random() * emptyCells.length)];
        
        board[bestMove] = "O";
        cells[bestMove].textContent = "O";

        let winner = checkWinner(board);
        if (winner) {
            endGame(winner);
        } else {
            currentPlayer = "X";
            statusDisplay.textContent = "Your turn!";
        }
    }

    function handleClick(event) {
        const index = parseInt(event.target.id);

        if (!gameActive || board[index] !== "") return;

        board[index] = "X";
        event.target.textContent = "X";

        let winner = checkWinner(board);
        if (winner) {
            endGame(winner);
        } else {
            currentPlayer = "O";
            statusDisplay.textContent = "AI is playing...";
            setTimeout(aiMove, 700); // Delay AI move slightly for effect
        }
    }

    function endGame(winner) {
        gameActive = false;
        if (winner === "draw") {
            statusDisplay.textContent = "It's a draw!";
        } else {
            statusDisplay.textContent = winner === "X" ? "You win! 🏆" : "AI wins! 😞";
        }

        // ✅ Send result to Django backend
        fetch("/update-tic-tac-toe-score/", {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
            body: JSON.stringify({ result: winner === "X" ? "win" : winner === "O" ? "loss" : "draw" })
        }).then(response => response.json())
        .then(data => console.log("Score updated:", data))
        .catch(error => console.error("Error updating score:", error));
    }

    function resetGame() {
        board = ["", "", "", "", "", "", "", "", ""];
        cells.forEach(cell => {
            cell.textContent = "";
        });
        gameActive = true;
        currentPlayer = "X";
        statusDisplay.textContent = "Player X's Turn";
    }

    cells.forEach(cell => cell.addEventListener("click", handleClick));
    resetButton.addEventListener("click", resetGame);

    statusDisplay.textContent = "Your turn!";
});
