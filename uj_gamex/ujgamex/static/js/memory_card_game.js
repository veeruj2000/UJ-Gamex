const cardsArray = ['🍎', '🍌', '🍇', '🍉', '🍎', '🍌', '🍇', '🍉', '🍓', '🥑', '🍓', '🥑', '🍍', '🍒', '🍍', '🍒'];
let gameBoard = document.getElementById('gameBoard');
let movesCount = document.getElementById('moves');
let timerDisplay = document.getElementById('timer');
let winMessage = document.getElementById('win-message');
let resetButton = document.getElementById('reset');

let flippedCards = [];
let moves = 0;
let matchedPairs = 0;
let startTime;
let timerInterval;

// ✅ Shuffle function
function shuffle(array) {
    return array.sort(() => Math.random() - 0.5);
}

// ✅ Start Timer (Counts UP from 0s)
function startTimer() {
    startTime = Date.now(); // Capture the starting time
    timerDisplay.textContent = "0s"; // Display starts at 0

    clearInterval(timerInterval); // Prevent multiple intervals
    timerInterval = setInterval(() => {
        let elapsedTime = Math.floor((Date.now() - startTime) / 1000);
        timerDisplay.textContent = elapsedTime + "s";
    }, 1000);
}

// ✅ Initialize Game
function initGame() {
    gameBoard.innerHTML = ''; // Clear previous board
    moves = 0;
    matchedPairs = 0;
    flippedCards = [];
    movesCount.textContent = moves;
    winMessage.style.display = 'none';

    let shuffledCards = shuffle([...cardsArray]);
    shuffledCards.forEach(symbol => {
        let card = document.createElement('div');
        card.classList.add('card');
        card.dataset.symbol = symbol;

        let frontFace = document.createElement('div');
        frontFace.classList.add('front');

        let backFace = document.createElement('div');
        backFace.classList.add('back');
        backFace.textContent = symbol;

        card.appendChild(frontFace);
        card.appendChild(backFace);
        card.addEventListener('click', flipCard);
        gameBoard.appendChild(card);
    });

    startTimer(); // Start the stopwatch when game begins
}

// ✅ Flip Card Logic
function flipCard() {
    if (flippedCards.length < 2 && !this.classList.contains('flipped')) {
        this.classList.add('flipped');
        flippedCards.push(this);

        if (flippedCards.length === 2) {
            checkMatch();
        }
    }
}

// ✅ Check for a Match
function checkMatch() {
    moves++;
    movesCount.textContent = moves;

    let [card1, card2] = flippedCards;
    if (card1.dataset.symbol === card2.dataset.symbol) {
        flippedCards = [];
        matchedPairs++;

        if (matchedPairs === cardsArray.length / 2) {
            clearInterval(timerInterval); // Stop the timer
            let finalTime = Math.floor((Date.now() - startTime) / 1000); // Calculate final time

            winMessage.textContent = `🎉 You won in ${finalTime} seconds! 🎉`;
            winMessage.style.display = 'block';

            // ✅ Send Final Time to Backend Leaderboard
            fetch("/update-memory-score/", {
                method: "POST",
                headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
                body: JSON.stringify({ time_taken: finalTime })
            })
            .then(response => response.json())
            .then(data => console.log("Memory Game Score Updated:", data))
            .catch(error => console.error("Error updating memory score:", error));
        }
    } else {
        setTimeout(() => {
            card1.classList.remove('flipped');
            card2.classList.remove('flipped');
            flippedCards = [];
        }, 1000);
    }
}

// ✅ Check if Time Runs Out (Game Over)
function checkGameOver() {
    let elapsedTime = Math.floor((Date.now() - startTime) / 1000);
    if (elapsedTime >= 100) { // If time reaches 100s, game over
        clearInterval(timerInterval);
        winMessage.textContent = "⏳ Time’s up! Try again.";
        winMessage.style.display = 'block';
    }
}

// ✅ Run Game Over Check Every Second
setInterval(checkGameOver, 1000);

// ✅ Restart Game
resetButton.addEventListener('click', initGame);

// ✅ Start Game on Page Load
initGame();

// ✅ Get CSRF Token for AJAX Requests
function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}
