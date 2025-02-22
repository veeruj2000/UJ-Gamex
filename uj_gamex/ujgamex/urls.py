# App-Specific URL Routing
from django.urls import path
from . import views  # Import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tic-tac-toe/", views.tic_tac_toe, name="tic_tac_toe"),
    path("update_score/", views.update_score, name="update_score"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("about/", views.about, name="about"),
    path("leaderboard/", views.leaderboard_view, name="leaderboard"),  # ✅ Leaderboard route
    path("update-leaderboard/<str:result>/", views.update_leaderboard, name="update_leaderboard"),  # ✅ Update leaderboard
]
