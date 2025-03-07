from django.db import models
from django.contrib.auth.models import User
from django.db.models import F

# ✅ Generic Leaderboard Model for all games
class GameLeaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to Django's User model
    game_name = models.CharField(max_length=50)  # Store game type
    wins = models.IntegerField(default=0)  # Track wins
    losses = models.IntegerField(default=0)  # Track losses
    draws = models.IntegerField(default=0)  # Track draws

    @property
    def final_score(self):
        return self.wins - self.losses  # Calculate final score

    def update_score(self, result):
        if result == "win":
            self.wins = F("wins") + 1
        elif result == "loss":
            self.losses = F("losses") + 1
        # Removed the faulty draw update logic
        self.save(update_fields=["wins", "losses"])

    def __str__(self):
        return f"{self.user.username} - {self.game_name} - Score: {self.final_score}"


# ✅ Tic-Tac-Toe Leaderboard Model
class TicTacToeLeaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)  # Added this field

    @property
    def final_score(self):
        return self.wins - self.losses  # Modify if draws should affect the score

    def __str__(self):
        return f"{self.user.username} - Tic-Tac-Toe - Score: {self.final_score}"



# ✅ Rock-Paper-Scissors Leaderboard Model
class RPSLeaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)  # Added this field
    final_score = models.IntegerField(default=0)

    @property
    def final_score(self):
        return self.wins - self.losses  # Modify if draws should affect the score

    def __str__(self):
        return f"{self.user.username} - Rock-Paper-Scissors - Score: {self.final_score}"


# ✅ Memory Card Game Leaderboard Model
class MemoryLeaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    matches_found = models.IntegerField(default=0)  # Count of correct matches
    moves_taken = models.IntegerField(default=0)  # Total moves used
    final_score = models.IntegerField(default=0)  # Score calculation

    def update_memory_score(self, matches, moves):
        self.matches_found = F("matches_found") + matches
        self.moves_taken = F("moves_taken") + moves
        self.final_score = F("final_score") + (matches * 10 - moves)
        self.save(update_fields=["matches_found", "moves_taken", "final_score"])

    def __str__(self):
        return f"{self.user.username} - Memory Card - Score: {self.final_score}"


# ✅ Snake Game Model
class SnakeLeaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date_played = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"{self.user.username} - {self.score}"



# ✅ Game Review Model (For all games)
class GameReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=50)
    review_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game_name} Review"


class ChessLeaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    final_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Score: {self.final_score}"