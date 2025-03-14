# App-Specific URL Routing
from django.urls import path
from . import views  # Import views
from .views import rock_paper_scissors_leaderboard, update_rps_score, get_rps_leaderboard

urlpatterns = [
    path("", views.home, name="home"),
    path("tic-tac-toe/", views.tic_tac_toe, name="tic_tac_toe"),   #for page rendering
    path("update_score/", views.update_score, name="update_score"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("about/", views.about, name="about"),    #for page rendering
    path("leaderboard/", views.leaderboard_view, name="leaderboard"),  # ✅ Leaderboard route
    path("update-leaderboard/<str:result>/", views.update_leaderboard, name="update_leaderboard"),  # ✅ Update leaderboard
    path('rock-paper-scissors/', views.rock_paper_scissors, name='rock_paper_scissors'),    #for rock-paper-scissors
    path('play-rock-paper-scissors/<str:player_choice>/', views.play_rock_paper_scissors, name='play_rock_paper_scissors'), #for rock-paper-scissors
    path('rock-paper-scissors-leaderboard/', rock_paper_scissors_leaderboard, name='rps_leaderboard'),
    path("update_rps_score/", update_rps_score, name="update_rps_score"),
    path("get_rps_leaderboard/", get_rps_leaderboard, name="get_rps_leaderboard"),
    path('api/rps-leaderboard/', get_rps_leaderboard, name='get_rps_leaderboard'),
    path("memory-card-game/", views.memory_card_game, name="memory_card_game"),
    path("memory-leaderboard/", views.memory_leaderboard, name="memory_leaderboard"),
    path("snake-game/", views.snake_game, name="snake_game"),
    path("snake-leaderboard/", views.snake_leaderboard, name="snake_leaderboard"),
    path("chess-game/", views.chess_game, name="chess_game"),
    path("update-chess-score/", views.update_chess_score, name="update_chess_score"),
    path("chess-leaderboard/", views.chess_leaderboard, name="chess_leaderboard"),
    path("ludo/", views.ludo_game, name="ludo"),
]
