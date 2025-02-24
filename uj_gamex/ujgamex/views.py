from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from .models import RPSLeaderboard
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import GameScore, Review, Score, Leaderboard, RockPaperScissorsLeaderboard
import random


# -------------------- HOME & BASIC PAGES --------------------

def home(request):
    scores = GameScore.objects.order_by("-score")[:5]  # Fetch top 5 scores
    reviews = Review.objects.all()  # Fetch all reviews
    tic_tac_toe_leaderboard = Leaderboard.objects.all().order_by('-wins', 'losses')
    rps_leaderboard = RockPaperScissorsLeaderboard.objects.all().order_by('-wins', 'losses')

    return render(request, 'home.html', {
        'scores': scores,
        'reviews': reviews,
        'tic_tac_toe_leaderboard': tic_tac_toe_leaderboard,
        'rps_leaderboard': rps_leaderboard
    })


def about(request):
    return render(request, 'about.html')


# -------------------- AUTHENTICATION --------------------

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
    return render(request, "login.html")

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ✅ Auto-login after successful registration
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect("home")


# -------------------- GAMES --------------------

@login_required
def tic_tac_toe(request):
    return render(request, "tic_tac_toe.html")


# -------------------- SCORE & LEADERBOARD --------------------

@login_required
def update_score(request):
    """ Update the user's score based on the game result. """
    if request.method == "POST":
        result = request.POST.get("result")  # win, loss, or draw
        user = request.user

        if result not in ["win", "loss", "draw"]:
            return JsonResponse({"status": "error", "message": "Invalid result"}, status=400)

        # ✅ Update Score Model
        user_score, _ = Score.objects.get_or_create(user=user)
        Score.objects.filter(user=user).update(
            wins=F("wins") + (1 if result == "win" else 0),
            losses=F("losses") + (1 if result == "loss" else 0),
            draws=F("draws") + (1 if result == "draw" else 0),
        )

        # ✅ Update Leaderboard Model
        Leaderboard.objects.get_or_create(user=user)
        Leaderboard.objects.filter(user=user).update(
            wins=F("wins") + (1 if result == "win" else 0),
            losses=F("losses") + (1 if result == "loss" else 0),
        )

        return JsonResponse({"status": "success", "message": "Score updated successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@login_required
def update_leaderboard(request, result):
    """ Update the leaderboard when a user wins or loses a game. """
    user = request.user

    if result not in ["win", "loss"]:
        return JsonResponse({"status": "error", "message": "Invalid result"}, status=400)

    Leaderboard.objects.get_or_create(user=user)
    Leaderboard.objects.filter(user=user).update(
        wins=F("wins") + (1 if result == "win" else 0),
        losses=F("losses") + (1 if result == "loss" else 0),
    )

    return JsonResponse({"status": "success", "message": "Leaderboard updated successfully!"})


def leaderboard_view(request):
    tic_tac_toe_leaderboard = Leaderboard.objects.all().order_by('-wins', 'losses')
    rps_leaderboard = RockPaperScissorsLeaderboard.objects.all().order_by('-wins', 'losses')

    return render(request, "leaderboard.html", {
        "tic_tac_toe_leaderboard": tic_tac_toe_leaderboard,
        "rps_leaderboard": rps_leaderboard
    })



# -------------------- ROCK PAPER SCISSORS --------------------
@login_required
def rock_paper_scissors(request):
    """ Render the Rock Paper Scissors game page. """
    return render(request, 'rock_paper_scissors.html')

@login_required
def play_rock_paper_scissors(request, player_choice):
    """ Play Rock Paper Scissors and update the leaderboard accordingly. """
    choices = ["rock", "paper", "scissors"]
    computer_choice = random.choice(choices)
    user = request.user

    if player_choice not in choices:
        return JsonResponse({"status": "error", "message": "Invalid choice"}, status=400)

    rps_leaderboard_entry, _ = RockPaperScissorsLeaderboard.objects.get_or_create(user=user)

    if player_choice == computer_choice:
        result = "It's a tie! 🤝"
    elif (player_choice == "rock" and computer_choice == "scissors") or \
         (player_choice == "paper" and computer_choice == "rock") or \
         (player_choice == "scissors" and computer_choice == "paper"):
        result = f"You win! 🎉 (Computer chose {computer_choice})"
        rps_leaderboard_entry.wins += 1
    else:
        result = f"You lose! 😢 (Computer chose {computer_choice})"
        rps_leaderboard_entry.losses += 1

    rps_leaderboard_entry.save()  # ✅ Save changes

    return JsonResponse({"result": result})


def rock_paper_scissors_leaderboard(request):
    rps_leaderboard = RockPaperScissorsLeaderboard.objects.all().order_by('-wins', 'losses')
    return render(request, 'leaderboard_rock_paper_scissors.html', {'leaderboard': rps_leaderboard})

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import RockPaperScissorsLeaderboard
from django.contrib.auth.decorators import login_required
import json

# API to update scores
@login_required
def update_rps_score(request):
    if request.method == "POST":
        data = json.loads(request.body)  # Get JSON data from request
        user = request.user  # Get the logged-in user
        result = data.get("result")  # "win" or "lose"

        leaderboard, created = RockPaperScissorsLeaderboard.objects.get_or_create(user=user)

        if result == "win":
            leaderboard.wins += 1
        elif result == "lose":
            leaderboard.losses += 1

        # Calculate final score (Example: wins - losses)
        leaderboard.final_score = leaderboard.wins - leaderboard.losses
        leaderboard.save()

        return JsonResponse({"success": True, "wins": leaderboard.wins, "losses": leaderboard.losses, "final_score": leaderboard.final_score})
    
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


# API to get leaderboard data
def get_rps_leaderboard(request):
    leaderboard_data = RPSLeaderboard.objects.order_by('-final_score')[:10]  # Get top 10 players
    leaderboard = [
        {
            "rank": index + 1,
            "player": entry.user.username,
            "wins": entry.wins,
            "losses": entry.losses,
            "final_score": entry.final_score,
        }
        for index, entry in enumerate(leaderboard_data)
    ]
    return JsonResponse({"leaderboard": leaderboard})