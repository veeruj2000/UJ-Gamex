from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.utils.timezone import now

# ✅ Tic-Tac-Toe Leaderboard Model
class TicTacToeLeaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    @property
    def final_score(self):
        return self.wins - self.losses  # Score = Wins - Losses

    def __str__(self):
        return f"{self.user.username} - Tic-Tac-Toe - Score: {self.final_score}"


# ✅ Rock-Paper-Scissors Leaderboard Model
class RPSLeaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)  # Draws are tracked but don’t affect score

    @property
    def final_score(self):
        return self.wins - self.losses  # Only wins and losses affect the score

    def __str__(self):
        return f"{self.user.username} - RPS - Score: {self.final_score}"



# ✅ Memory Card Game Leaderboard Model (Ranking by least time taken)
class MemoryLeaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    time_taken = models.FloatField(default=100)  # Time in seconds (default max)
    
    class Meta:
        ordering = ["time_taken"]  # Rank by least time taken

    def update_score(self, new_time):
        """ Update only if the new time is better (lower) """
        if new_time < self.time_taken:
            self.time_taken = new_time
            self.save(update_fields=["time_taken"])

    def __str__(self):
        return f"{self.user.username} - Memory Cards - Time: {self.time_taken}s"


# ✅ Snake Game Leaderboard (Ranking by highest score)
class SnakeLeaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        ordering = ["-score"]  # Rank by highest score

    def update_score(self, new_score):
        """ Update only if the new score is higher """
        if new_score > self.score:
            self.score = new_score
            self.save(update_fields=["score"])

    def __str__(self):
        return f"{self.user.username} - Snake - Score: {self.score}"


# ✅ Ludo Game Leaderboard (Only for the current match, not stored permanently)
class LudoMatchLeaderboard(models.Model):
    player = models.CharField(max_length=50)  # Store player name
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player} - Ludo Score: {self.score}"


# ✅ Game Review Model (For all games)
class GameReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=50)
    review_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game_name} Review"
