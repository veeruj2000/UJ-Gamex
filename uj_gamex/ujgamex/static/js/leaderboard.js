document.addEventListener("DOMContentLoaded", function () {
    loadLeaderboard("get-tic-tac-toe-leaderboard", "tic-tac-toe-leaderboard", ["rank", "user", "wins", "losses", "final_score"]);
    loadLeaderboard("get-rps-leaderboard", "rps-leaderboard", ["rank", "player", "wins", "losses", "final_score"]);
    loadLeaderboard("get-memory-leaderboard", "memory-leaderboard", ["rank", "user", "time_taken"]);
    loadLeaderboard("snake-leaderboard", "snake-leaderboard", ["rank", "player", "score"]);
});

function loadLeaderboard(apiEndpoint, tableId, columns) {
    fetch(`/${apiEndpoint}/`)
        .then(response => response.json())
        .then(data => {
            let table = document.getElementById(tableId);
            table.innerHTML = ""; // Clear old data

            if (data.leaderboard.length === 0) {
                table.innerHTML = `<tr><td colspan="${columns.length}" class="text-center">No data available.</td></tr>`;
            } else {
                data.leaderboard.forEach(entry => {
                    let row = "<tr>";
                    columns.forEach(col => row += `<td>${entry[col]}</td>`);
                    row += "</tr>";
                    table.innerHTML += row;
                });
            }
        })
        .catch(error => console.error(`Error loading ${tableId}:`, error));
}
