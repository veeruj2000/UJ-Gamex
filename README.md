# UJ GameX 
### An Online Gaming Platform 🎮🚀
UJ GameX is an interactive, web-based multiplayer gaming platform that provides a fun and engaging experience for users coming up with more days with a daily streak. The platform currently features Tic-Tac-Toe and Rock Paper Scissors with a seamless user experience that includes authentication-based access, leaderboards and real-time score tracking. The project is built using Django for backend and JavaScript for frontend, ensuring smooth gameplay and efficient data handling.

📌 Key Highlights:
✔️ User Authentication – Mandatory login to play games 🔐
✔️ Leaderboard System – Tracks top-performing players 🏆
✔️ Real-time Score Updates – Dynamic gameplay 📊
✔️ Interactive UI – Responsive design with smooth animations ✨
✔️ Secure Backend – Django framework with SQLite database 🛠️
✔️ Deployed on Netlify & Render – Seamless hosting experience 🌍

##📌 Game Modules & Features
## 1️⃣ Tic-Tac-Toe (Artificial Intelligence--Python--Django--HTML--CSS-Javascript--Graphic Design)
Tic-Tac-Toe is a two-player game where players take turns marking spaces in a 3x3 grid. The game follows standard rules and offers the following features:

Turn-Based Gameplay 🔄 – Ensures players play alternatively.
Winner & Draw Detection 🏆 – Checks for three-in-a-row conditions.
Real-time Score Tracking 📊 – Keeps track of user wins and losses.
User Authentication Required 🔐 – Prevents anonymous play.
Responsive UI & Smooth Animations ✨

## 2️⃣ Rock Paper Scissors (Python--Django--HTML--CSS-Javascript--Graphic Design)
A fast-paced one-vs-one game where users select between Rock, Paper, or Scissors. The game logic follows the standard rules:
Rock beats Scissors, Scissors beats Paper, and Paper beats Rock.
Authentication Required 🔐 – Only logged-in users can play.
Leaderboard System 🎖️ – Tracks and displays top players.
Real-time Score Updates 📈 – Users' best scores are stored and displayed.
User-friendly UI 🖥️ – Intuitive game interface.

📌 Technologies Used
Component	Technology Stack
Frontend	HTML, CSS, JavaScript
Backend	Django (Python)
Database	SQLite
Deployment	Netlify (Frontend), Render (Backend)
Authentication	Django Authentication
Game Logic	JavaScript (Frontend), Django (Backend)

📌 Leaderboard System
Each game has a leaderboard that tracks players’ performance.
Scores are stored in the database and retrieved dynamically.
Users can check their ranking and progress over time.
Data is displayed in a descending order of scores.

📌 User Authentication & Game Access
Login is mandatory before accessing any game.
If a user clicks "Play Game" without logging in, they are redirected to the login page.
Upon successful authentication, users are directed to the game page.
This ensures security, fair gameplay, and personalized experience.

📌 Backend API Endpoints
Method	Endpoint	Description
POST	/api/save-rps-score/	Saves Rock Paper Scissors game scores
GET	/api/rps-leaderboard/	Retrieves top players for Rock Paper Scissors
GET	/api/tic-tac-toe-leaderboard/	Retrieves Tic-Tac-Toe leaderboard
POST	/api/login/	Authenticates users and starts a session

📌 Future Enhancements 🚀
✔️ Live Games with WebSockets – Real-time gameplay interaction.
✔️ AI Opponent Mode – Play against a smart AI.
✔️ More Games (Chess, Ludo, Snake, etc.) – Expanding the game collection.
✔️ User Profiles & Avatars – Personalized gaming experience.

UJ GameX is a fun, competitive, and engaging multiplayer gaming platform built for interactive browser-based gaming. 🎉
