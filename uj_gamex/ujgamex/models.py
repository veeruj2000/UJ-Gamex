#Database Models
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Linked to Django's User model
    wins = models.IntegerField(default=0)  # Track wins
    losses = models.IntegerField(default=0)  # Track losses

    @property
    def final_score(self):
        return self.wins - self.losses  # Calculate final score (win - loss)

    def __str__(self):
        return f"{self.user.username} - Wins: {self.wins}, Losses: {self.losses}, Score: {self.final_score}"


class GameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=50)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game_name} - {self.score}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=50)
    review_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game_name}"

class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Wins: {self.wins}, Losses: {self.losses}, Draws: {self.draws}"