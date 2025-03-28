document.addEventListener("DOMContentLoaded", function () {
    loadTicTacToeLeaderboard();
    loadRPSLeaderboard();
    loadMemoryLeaderboard();
    loadSnakeLeaderboard();
});

// ✅ Load Tic-Tac-Toe Leaderboard
function loadTicTacToeLeaderboard() {
    fetch("/tic-tac-toe-leaderboard/") // Fetch from Django API
    .then(response => response.json())
    .then(data => {
        let leaderboardTable = document.getElementById("tic-tac-toe-leaderboard");
        leaderboardTable.innerHTML = "";

        if (data.length === 0) {
            leaderboardTable.innerHTML = `<tr><td colspan="5" class="text-center">No players have played yet.</td></tr>`;
        } else {
            data.forEach((player, index) => {
                let row = `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${player.user}</td>
                        <td>${player.wins}</td>
                        <td>${player.losses}</td>
                        <td>${player.final_score}</td>
                    </tr>`;
                leaderboardTable.innerHTML += row;
            });
        }
    })
    .catch(error => console.error("Error loading Tic-Tac-Toe leaderboard:", error));
}

// ✅ Load Rock-Paper-Scissors Leaderboard
function loadRPSLeaderboard() {
    fetch("/get_rps_leaderboard/") 
    .then(response => response.json())
    .then(data => {
        let leaderboardTable = document.getElementById("rps-leaderboard");
        leaderboardTable.innerHTML = "";

        if (data.leaderboard.length === 0) {
            leaderboardTable.innerHTML = `<tr><td colspan="5" class="text-center">No players have played yet.</td></tr>`;
        } else {
            data.leaderboard.forEach((player, index) => {
                let row = `
                    <tr>
                        <td>${player.rank}</td>
                        <td>${player.player}</td>
                        <td>${player.wins}</td>
                        <td>${player.losses}</td>
                        <td>${player.final_score}</td>
                    </tr>`;
                leaderboardTable.innerHTML += row;
            });
        }
    })
    .catch(error => console.error("Error loading RPS leaderboard:", error));
}

// ✅ Load Memory Card Game Leaderboard
function loadMemoryLeaderboard() {
    fetch("/memory-leaderboard/") 
    .then(response => response.json())
    .then(data => {
        let leaderboardTable = document.getElementById("memory-leaderboard");
        leaderboardTable.innerHTML = "";

        if (data.length === 0) {
            leaderboardTable.innerHTML = `<tr><td colspan="5" class="text-center">No players have played yet.</td></tr>`;
        } else {
            data.forEach((player, index) => {
                let row = `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${player.user}</td>
                        <td>${player.matches_found}</td>
                        <td>${player.moves_taken}</td>
                        <td>${player.final_score}</td>
                    </tr>`;
                leaderboardTable.innerHTML += row;
            });
        }
    })
    .catch(error => console.error("Error loading Memory leaderboard:", error));
}

// ✅ Load SnakeX Leaderboard
function loadSnakeLeaderboard() {
    fetch("/snake-leaderboard/") 
    .then(response => response.json())
    .then(data => {
        let leaderboardTable = document.getElementById("snake-leaderboard");
        leaderboardTable.innerHTML = "";

        if (data.length === 0) {
            leaderboardTable.innerHTML = `<tr><td colspan="3" class="text-center">No players have played yet.</td></tr>`;
        } else {
            data.forEach((player, index) => {
                let row = `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${player.user}</td>
                        <td>${player.score}</td>
                    </tr>`;
                leaderboardTable.innerHTML += row;
            });
        }
    })
    .catch(error => console.error("Error loading Snake leaderboard:", error));
}
