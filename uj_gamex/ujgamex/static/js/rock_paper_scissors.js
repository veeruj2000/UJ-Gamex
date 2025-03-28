let userScore = 0;
let computerScore = 0;

function playGame(userChoice) {
    let choices = ["rock", "paper", "scissors"];
    let computerChoice = choices[Math.floor(Math.random() * 3)];
    let result = "";

    // Determine game result
    if (userChoice === computerChoice) {
        result = "draw";
    } else if (
        (userChoice === "rock" && computerChoice === "scissors") ||
        (userChoice === "paper" && computerChoice === "rock") ||
        (userChoice === "scissors" && computerChoice === "paper")
    ) {
        result = "win";
        userScore++;
    } else {
        result = "lose";
        computerScore++;
    }

    // Update scores on UI
    document.getElementById("user_score").innerText = userScore;
    document.getElementById("computer_score").innerText = computerScore;
    document.getElementById("comp_choice").innerHTML = `Computer chose <span>${computerChoice.toUpperCase()}</span>`;
    document.getElementById("user_choice").innerHTML = `You chose <span>${userChoice.toUpperCase()}</span>`;

    // Send updated score to backend
    if (result !== "draw") {
        fetch("/update_rps_score/", {  // Ensure URL matches Django urls.py
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()  // Ensure correct CSRF token
            },
            body: JSON.stringify({ result: result })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Score Updated:", data);
        })
        .catch(error => console.error("Error updating score:", error));
    }
}

// Function to retrieve CSRF token from cookies
function getCSRFToken() {
    let csrfToken = document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
    return csrfToken || "";
}
