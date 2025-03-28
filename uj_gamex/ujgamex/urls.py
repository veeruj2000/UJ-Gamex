# App-Specific URL Routing
from django.urls import path
from . import views  

urlpatterns = [
    # Home & Authentication
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),

    # Tic-Tac-Toe
    path("tic-tac-toe/", views.tic_tac_toe, name="tic_tac_toe"),
    path("get-tic-tac-toe-leaderboard/", views.get_tic_tac_toe_leaderboard, name="get_tic_tac_toe_leaderboard"),
    path("update-tic-tac-toe-score/", views.update_tic_tac_toe_score, name="update_tic_tac_toe_score"),

    # Rock-Paper-Scissors
    path("rock-paper-scissors/", views.rock_paper_scissors, name="rock_paper_scissors"),
    path("get-rps-leaderboard/", views.get_rps_leaderboard, name="get_rps_leaderboard"),
    path("update_rps_score/", views.update_rps_score, name="update_rps_score"),


    # Memory Card Game
    path("memory-card-game/", views.memory_card_game, name="memory_card_game"),
    path("get-memory-leaderboard/", views.get_memory_leaderboard, name="get_memory_leaderboard"),
    path("update-memory-score/", views.update_memory_score, name="update_memory_score"),

    # Snake Game
    path("snake-game/", views.snake_game, name="snake_game"),
    path("snake-leaderboard/", views.get_snake_leaderboard, name="get_snake_leaderboard"),
    path("update-snake-score/", views.update_snake_score, name="update_snake_score"),

    # Chess
    path("chess-game/", views.chess_game, name="chess_game"),
    path("update-chess-score/", views.update_chess_score, name="update_chess_score"),

    # Ludo (Leaderboard shown in-game)
    path("ludo/", views.ludo_game, name="ludo"),
    path("update-ludo-leaderboard/", views.update_ludo_leaderboard, name="update_ludo_leaderboard"),
    path("get-ludo-leaderboard/", views.get_ludo_leaderboard, name="get_ludo_leaderboard"),
]
