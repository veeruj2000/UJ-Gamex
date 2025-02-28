// Snake Game Update with Leaderboard Integration
// Features Fixed & Enhanced:
// - Ensured canvas visibility
// - Proper Start & Pause button handling
// - Initial render fix
// - Stronger grid line contrast
// - Score tracking & leaderboard update

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const startButton = document.getElementById("startButton");
const pauseButton = document.getElementById("pauseButton");
const scoreDisplay = document.getElementById("score");

canvas.width = 1300; // Increased game area size
canvas.height = 500;

const box = 20;
let speed = 90; // Increased speed by doubling it
let snake = [{ x: 200, y: 200 }];
let direction = "RIGHT";
let food = { x: Math.floor(Math.random() * (canvas.width / box)) * box, y: Math.floor(Math.random() * (canvas.height / box)) * box };
let gameInterval;
let isPaused = true;
let score = 0; // Score Tracking

function drawGrid() {
    ctx.strokeStyle = "rgba(255, 255, 255, 0.15)"; // Reduced grid opacity
    for (let x = 0; x < canvas.width; x += box) {
        for (let y = 0; y < canvas.height; y += box) {
            ctx.strokeRect(x, y, box, box);
        }
    }
}

function draw() {
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    drawGrid();
    
    ctx.fillStyle = "red";
    ctx.fillRect(food.x, food.y, box, box);
    
    ctx.fillStyle = "green";
    snake.forEach((segment) => {
        ctx.fillRect(segment.x, segment.y, box, box);
    });
    
    scoreDisplay.innerText = `Score: ${score}`; // Update Score Display
    
    if (isPaused) return;
    
    let head = { ...snake[0] };
    switch (direction) {
        case "UP": head.y -= box; break;
        case "DOWN": head.y += box; break;
        case "LEFT": head.x -= box; break;
        case "RIGHT": head.x += box; break;
    }
    
    // Wall wrap-around logic
    head.x = (head.x + canvas.width) % canvas.width;
    head.y = (head.y + canvas.height) % canvas.height;
    
    // Check self-collision
    if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
        clearInterval(gameInterval);
        alert(`Game Over! Your Score: ${score}`);
        sendScoreToBackend(score); // Send Score to Backend
        return;
    }
    
    snake.unshift(head);
    if (head.x === food.x && head.y === food.y) {
        score += 10; // Increase Score
        food = { x: Math.floor(Math.random() * (canvas.width / box)) * box, y: Math.floor(Math.random() * (canvas.height / box)) * box };
    } else {
        snake.pop();
    }
}

function changeDirection(event) {
    const key = event.key;
    if (key === "ArrowUp" && direction !== "DOWN") direction = "UP";
    if (key === "ArrowDown" && direction !== "UP") direction = "DOWN";
    if (key === "ArrowLeft" && direction !== "RIGHT") direction = "LEFT";
    if (key === "ArrowRight" && direction !== "LEFT") direction = "RIGHT";
    if (key === " ") togglePause();
    event.preventDefault();
}

function togglePause() {
    isPaused = !isPaused;
    if (!isPaused) {
        gameInterval = setInterval(draw, speed);
    } else {
        clearInterval(gameInterval);
    }
}

function startGame() {
    isPaused = false;
    score = 0; // Reset Score
    snake = [{ x: 200, y: 200 }];
    direction = "RIGHT";
    clearInterval(gameInterval);
    gameInterval = setInterval(draw, speed);
    draw();
}

// ✅ Function to Send Score to Django API
function sendScoreToBackend(finalScore) {
    fetch("/update-snake-score/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(), // Get CSRF Token
        },
        body: JSON.stringify({ score: finalScore }),
    })
    .then(response => response.json())
    .then(data => console.log("Score Updated:", data))
    .catch(error => console.error("Error updating score:", error));
}

// ✅ Function to Fetch and Update Leaderboard
function loadSnakeLeaderboard() {
    fetch("/get-snake-leaderboard/")
    .then(response => response.json())
    .then(data => {
        let leaderboardTable = document.getElementById("snake-leaderboard");
        leaderboardTable.innerHTML = "";

        if (data.leaderboard.length === 0) {
            leaderboardTable.innerHTML = `<tr><td colspan="5" class="text-center">No players have played yet.</td></tr>`;
        } else {
            data.leaderboard.forEach((player, index) => {
                let row = `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${player.username}</td>
                        <td>${player.score}</td>
                    </tr>`;
                leaderboardTable.innerHTML += row;
            });
        }
    })
    .catch(error => console.error("Error loading leaderboard:", error));
}

document.addEventListener("DOMContentLoaded", loadSnakeLeaderboard);
document.addEventListener("keydown", changeDirection);
startButton.addEventListener("click", startGame);
pauseButton.addEventListener("click", togglePause);

// ✅ Function to Get CSRF Token
function getCSRFToken() {
    return document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}