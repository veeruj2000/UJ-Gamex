from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Leaderboard

class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'wins', 'losses', 'final_score')

admin.site.register(Leaderboard, LeaderboardAdmin)


User = get_user_model()  # Get the default User model

# Check if the User model is already registered before registering
if not admin.site.is_registered(User):
    admin.site.register(User)
