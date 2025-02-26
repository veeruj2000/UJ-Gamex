from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import GameLeaderboard, TicTacToeLeaderboard, RPSLeaderboard, MemoryLeaderboard, GameReview

# Get Django's User model
User = get_user_model()

# Register User model if not already registered
try:
    admin.site.register(User)
except admin.sites.AlreadyRegistered:
    pass  # Ignore if already registered

# Register Leaderboards
admin.site.register(GameLeaderboard)
admin.site.register(TicTacToeLeaderboard)
admin.site.register(RPSLeaderboard)
admin.site.register(MemoryLeaderboard)

# Register Game Reviews
admin.site.register(GameReview)
