document.addEventListener("DOMContentLoaded", () => {
    const cards = [
        "🍎", "🍎", "🍌", "🍌", "🍉", "🍉",
        "🍇", "🍇", "🥭", "🥭", "🍍", "🍍"
    ];
    let flippedCards = [];
    let matchedCards = [];
    let score = 0;

    const gameBoard = document.getElementById("game-board");
    cards.sort(() => Math.random() - 0.5);

    cards.forEach((symbol, index) => {
        let card = document.createElement("div");
        card.classList.add("card");
        card.dataset.symbol = symbol;
        card.innerHTML = "❓";
        card.onclick = () => flipCard(card);
        gameBoard.appendChild(card);
    });

    function flipCard(card) {
        if (flippedCards.length < 2 && !matchedCards.includes(card)) {
            card.innerHTML = card.dataset.symbol;
            flippedCards.push(card);
            
            if (flippedCards.length === 2) {
                setTimeout(checkMatch, 500);
            }
        }
    }

    function checkMatch() {
        if (flippedCards[0].dataset.symbol === flippedCards[1].dataset.symbol) {
            matchedCards.push(...flippedCards);
            score += 10;
            document.getElementById("score").innerText = `Score: ${score}`;
        } else {
            flippedCards.forEach(card => (card.innerHTML = "❓"));
        }
        flippedCards = [];

        if (matchedCards.length === cards.length) {
            alert("Congratulations! You won!");
        }
    }

    window.restartGame = function() {
        location.reload();
    };
});
