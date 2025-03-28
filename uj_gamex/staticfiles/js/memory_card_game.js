const cardsArray = ['🍎', '🍌', '🍇', '🍉', '🍎', '🍌', '🍇', '🍉', '🍓', '🥑', '🍓', '🥑', '🍍', '🍒', '🍍','🍒'];
        let gameBoard = document.getElementById('gameBoard');
        let movesCount = document.getElementById('moves');
        let timerDisplay = document.getElementById('timer');
        let winMessage = document.getElementById('win-message');
        let resetButton = document.getElementById('reset');
        let flippedCards = [];
        let moves = 0;
        let matchedPairs = 0;
        let timeLeft = 100;
        let timer;

        // Shuffle function
        function shuffle(array) {
            return array.sort(() => Math.random() - 0.5);
        }

        // Start the timer
        function startTimer() {
            timeLeft = 100;
            timerDisplay.textContent = timeLeft + "s";
            clearInterval(timer);

            timer = setInterval(() => {
                timeLeft--;
                timerDisplay.textContent = timeLeft + "s";

                if (timeLeft <= 10) {
                    timerDisplay.style.backgroundColor = "#ff6b6b"; // Change color to red if time is low
                }

                if (timeLeft <= 0) {
                    clearInterval(timer);
                    alert('⏳ Time’s up! Try again.');
                    initGame();
                }
            }, 1000);
        }

        // Initialize game
        function initGame() {
            gameBoard.innerHTML = '';
            moves = 0;
            matchedPairs = 0;
            movesCount.textContent = moves;
            flippedCards = [];
            winMessage.style.display = 'none';
            timerDisplay.style.backgroundColor = "#ff4757";
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

            startTimer();
        }

        // Flip card
        function flipCard() {
            if (flippedCards.length < 2 && !this.classList.contains('flipped')) {
                this.classList.add('flipped');
                flippedCards.push(this);

                if (flippedCards.length === 2) {
                    checkMatch();
                }
            }
        }

        // Check for a match
        function checkMatch() {
            moves++;
            movesCount.textContent = moves;

            let [card1, card2] = flippedCards;
            if (card1.dataset.symbol === card2.dataset.symbol) {
                flippedCards = [];
                matchedPairs++;

                if (matchedPairs === cardsArray.length / 2) {
                    clearInterval(timer);
                    winMessage.style.display = 'block';
                }
            } else {
                setTimeout(() => {
                    card1.classList.remove('flipped');
                    card2.classList.remove('flipped');
                    flippedCards = [];
                }, 1000);
            }
        }

        // Restart game
        resetButton.addEventListener('click', initGame);

        // Start game on load
        initGame();