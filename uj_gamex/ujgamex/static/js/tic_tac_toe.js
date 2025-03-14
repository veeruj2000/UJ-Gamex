document.addEventListener("DOMContentLoaded", function () {
    let board = ["", "", "", "", "", "", "", "", ""];
    let currentPlayer = "X"; // User is X, AI is O
    let gameActive = true;

    const cells = document.querySelectorAll(".cell");
    const statusDisplay = document.getElementById("status");
    const resetButton = document.getElementById("reset");

    function checkWinner(board) {
        const winningCombinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], 
            [0, 3, 6], [1, 4, 7], [2, 5, 8], 
            [0, 4, 8], [2, 4, 6]
        ];
        for (let combo of winningCombinations) {
            let [a, b, c] = combo;
            if (board[a] && board[a] === board[b] && board[a] === board[c]) {
                return board[a]; // Return "X" or "O"
            }
        }
        return board.includes("") ? null : "draw"; // Return "draw" if no moves left
    }

    function aiMove() {
        if (!gameActive) return;
    
        let emptyCells = board
            .map((val, idx) => val === "" ? idx : null)
            .filter(val => val !== null);
    
        if (emptyCells.length === 0) return;
    
        let bestScore = -Infinity;
        let bestMove;
        
        // Use Minimax to find the best move
        for (let i = 0; i < board.length; i++) {
            if (board[i] === "") {
                board[i] = "O";
                let score = minimax(board, 0, false);
                board[i] = "";
                if (score > bestScore) {
                    bestScore = score;
                    bestMove = i;
                }
            }
        }
    
        let aiChoice;
        
        // 80% chance AI picks the best move, 20% chance it picks a random move
        if (Math.random() < 0.8) {
            aiChoice = bestMove;
        } else {
            aiChoice = emptyCells[Math.floor(Math.random() * emptyCells.length)];
        }
    
        // AI makes the chosen move
        board[aiChoice] = "O";
        cells[aiChoice].textContent = "O";
    
        let winner = checkWinner(board);
        if (winner) {
            endGame(winner);
        } else {
            currentPlayer = "X";
            statusDisplay.textContent = "Your turn!";
        }
    }
    

    const scores = { X: -10, O: 10, draw: 0 };

function minimax(board, depth, isMaximizing) {
    let winner = checkWinner(board);
    if (winner) return scores[winner];

    if (isMaximizing) {
        let bestScore = -Infinity;
        for (let i = 0; i < board.length; i++) {
            if (board[i] === "") {
                board[i] = "O";
                let score = minimax(board, depth + 1, false);
                board[i] = "";
                bestScore = Math.max(score, bestScore);
            }
        }
        return bestScore;
    } else {
        let bestScore = Infinity;
        for (let i = 0; i < board.length; i++) {
            if (board[i] === "") {
                board[i] = "X";
                let score = minimax(board, depth + 1, true);
                board[i] = "";
                bestScore = Math.min(score, bestScore);
            }
        }
        return bestScore;
    }
}

    

    function handleClick(event) {
        const index = parseInt(event.target.id); // Convert string ID to integer

        if (!gameActive || board[index] !== "") return;

        board[index] = "X";
        event.target.textContent = "X";

        console.log(`Player moved at index: ${index}`);

        let winner = checkWinner(board);
        if (winner) {
            endGame(winner);
        } else {
            currentPlayer = "O";
            statusDisplay.textContent = "AI is playing...";
            setTimeout(aiMove, 500); // Delay AI move slightly
        }
    }

    function endGame(winner) {
        gameActive = false;
        if (winner === "draw") {
            statusDisplay.textContent = "It's a draw!";
        } else {
            statusDisplay.textContent = (winner === "X") ? "You win!" : "AI wins!";
        }

        // Send the result to the backend
        fetch("/update_score/", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded", "X-CSRFToken": getCSRFToken() },
            body: `result=${winner === "X" ? "win" : winner === "O" ? "loss" : "draw"}`
        }).then(response => response.json())
        .then(data => console.log("Score updated:", data))
        .catch(error => console.error("Error updating score:", error));
    }

    function resetGame() {
        board = ["", "", "", "", "", "", "", "", ""];
        cells.forEach(cell => cell.textContent = "");
        gameActive = true;
        currentPlayer = "X";
        statusDisplay.textContent = "Player X's Turn";
    }

    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }

    cells.forEach(cell => cell.addEventListener("click", handleClick));
    resetButton.addEventListener("click", resetGame);

    statusDisplay.textContent = "Your turn!";
});
