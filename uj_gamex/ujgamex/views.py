from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.db.models import F
from .models import (
    GameLeaderboard, TicTacToeLeaderboard, RPSLeaderboard,
    MemoryLeaderboard, GameReview, SnakeLeaderboard, ChessLeaderboard
)
from django.utils.timezone import now

import random
import json


# -------------------- HOME & BASIC PAGES --------------------

def home(request):
    """ Render the home page with leaderboards and game scores. """
    scores = GameLeaderboard.objects.order_by("-wins", "losses")[:5]  # Fetch top 5 scores
    reviews = GameReview.objects.all()  # Fetch all reviews
    tic_tac_toe_leaderboard = TicTacToeLeaderboard.objects.order_by('-wins', 'losses')
    rps_leaderboard = RPSLeaderboard.objects.order_by('-wins', 'losses')

    return render(request, 'home.html', {
        'scores': scores,
        'reviews': reviews,
        'tic_tac_toe_leaderboard': tic_tac_toe_leaderboard,
        'rps_leaderboard': rps_leaderboard
    })


def about(request):
    """ Render the About page. """
    return render(request, 'about.html')


# -------------------- AUTHENTICATION --------------------

def login_user(request):
    """ Log in a user if credentials are valid. """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
    return render(request, "login.html")


def register_user(request):
    """ Register a new user and log them in automatically. """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def logout_user(request):
    """ Log out the current user and redirect to home. """
    logout(request)
    return redirect("home")


# -------------------- GAMES --------------------

@login_required
def tic_tac_toe(request):
    """ Render the Tic Tac Toe game page. """
    return render(request, "tic_tac_toe.html")


# -------------------- SCORE & LEADERBOARD --------------------

@login_required
def update_score(request):
    """ Update the user's score based on the game result. """
    if request.method == "POST":
        result = request.POST.get("result")  # Expected values: 'win', 'loss', 'draw'
        user = request.user

        if result not in ["win", "loss", "draw"]:
            return JsonResponse({"status": "error", "message": "Invalid result"}, status=400)

        # ✅ Update Game Leaderboard
        user_score, _ = GameLeaderboard.objects.get_or_create(user=user, game_name="General")
        GameLeaderboard.objects.filter(user=user, game_name="General").update(
            wins=F("wins") + (1 if result == "win" else 0),
            losses=F("losses") + (1 if result == "loss" else 0),
            draws=F("draws") + (1 if result == "draw" else 0),
        )

        return JsonResponse({"status": "success", "message": "Score updated successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@login_required
def update_leaderboard(request, result):
    """ Update the Tic-Tac-Toe leaderboard when a user wins or loses. """
    user = request.user

    if result not in ["win", "loss"]:
        return JsonResponse({"status": "error", "message": "Invalid result"}, status=400)

    TicTacToeLeaderboard.objects.get_or_create(user=user)
    TicTacToeLeaderboard.objects.filter(user=user).update(
        wins=F("wins") + (1 if result == "win" else 0),
        losses=F("losses") + (1 if result == "loss" else 0),
    )

    return JsonResponse({"status": "success", "message": "Leaderboard updated successfully!"})


def leaderboard_view(request):
    """ Display the leaderboards for different games. """
    tic_tac_toe_leaderboard = TicTacToeLeaderboard.objects.order_by('-wins', 'losses')
    rps_leaderboard = RPSLeaderboard.objects.order_by('-wins', 'losses')

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

    rps_leaderboard_entry, _ = RPSLeaderboard.objects.get_or_create(user=user)

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

    rps_leaderboard_entry.save()

    return JsonResponse({"result": result})


@login_required
def memory_card_game(request):
    """ Render the Memory Card Game page. """
    return render(request, "memory_card_game.html")


@login_required
def memory_leaderboard(request):
    """ Fetch and display the Memory Card Game leaderboard. """
    leaderboard = MemoryLeaderboard.objects.order_by('-final_score')[:10]
    return render(request, "memory_leaderboard.html", {"leaderboard": leaderboard})


# -------------------- ROCK PAPER SCISSORS API --------------------

@login_required
def update_rps_score(request):
    """ API to update Rock Paper Scissors scores. """
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        result = data.get("result")

        leaderboard, _ = RPSLeaderboard.objects.get_or_create(user=user)

        if result == "win":
            leaderboard.wins += 1
        elif result == "lose":
            leaderboard.losses += 1

        leaderboard.final_score = leaderboard.wins - leaderboard.losses
        leaderboard.save()

        return JsonResponse({"success": True, "wins": leaderboard.wins, "losses": leaderboard.losses, "final_score": leaderboard.final_score})
    
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


@login_required
def rock_paper_scissors_leaderboard(request):
    """ Render the Rock Paper Scissors leaderboard page. """
    leaderboard = RPSLeaderboard.objects.order_by('-final_score')[:10]
    return render(request, 'rock_paper_scissors_leaderboard.html', {"leaderboard": leaderboard})


def get_rps_leaderboard(request):
    """ API to fetch Rock Paper Scissors leaderboard. """
    leaderboard_data = RPSLeaderboard.objects.order_by('-final_score')[:10]
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

# -------------------- MEMORY CARD GAME LEADERBOARD --------------------

@login_required
def update_memory_score(request):
    """ API to update Memory Card Game scores. """
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        score = data.get("score")

        if not isinstance(score, int) or score < 0:
            return JsonResponse({"status": "error", "message": "Invalid score"}, status=400)

        leaderboard, _ = MemoryLeaderboard.objects.get_or_create(user=user)

        if score > leaderboard.final_score:  # Only update if the new score is higher
            leaderboard.final_score = score
            leaderboard.save()

        return JsonResponse({"status": "success", "new_score": leaderboard.final_score})
    
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

# -------------------- SNAKE GAME --------------------

@login_required
def snake_game(request):
    return render(request, "snake_game.html")

@login_required
def snake_leaderboard(request):
    leaderboard = SnakeLeaderboard.objects.all()
    return render(request, "snake_leaderboard.html", {"leaderboard": leaderboard})

@login_required
def update_snake_score(request):
    """API to update Snake Game leaderboard."""
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        score = data.get("score")

        if not isinstance(score, int) or score < 0:
            return JsonResponse({"status": "error", "message": "Invalid score"}, status=400)

        leaderboard_entry, _ = SnakeLeaderboard.objects.get_or_create(user=user)

        if score > leaderboard_entry.final_score:  # Only update if the new score is higher
            leaderboard_entry.final_score = score
            leaderboard_entry.save()

        return JsonResponse({"status": "success", "new_score": leaderboard_entry.final_score})
    
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

#---------------------- Chess Game ---------------------


@login_required
def chess_game(request):
    return render(request, "chess.html")  # Ensure chess.html exists in `templates/`

@login_required
@csrf_exempt
def update_chess_score(request):
    if request.method == "POST":
        data = json.loads(request.body)
        result = data.get("result")  # 'win' or 'loss'
        
        leaderboard, created = ChessLeaderboard.objects.get_or_create(player=request.user)
        
        if result == "win":
            leaderboard.wins += 1
        elif result == "loss":
            leaderboard.losses += 1
        
        leaderboard.score = leaderboard.wins - leaderboard.losses
        leaderboard.save()
        
        return JsonResponse({"message": "Score updated successfully!"})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

def chess_leaderboard(request):
    leaderboard = ChessLeaderboard.objects.order_by("-score")
    leaderboard_data = [
        {
            "player": entry.player.username,
            "wins": entry.wins,
            "losses": entry.losses,
            "score": entry.score,
        }
        for entry in leaderboard
    ]
    return JsonResponse(leaderboard_data, safe=False)


#-------------------- Ludo Game Page --------------------

def ludo_game(request):
    """ Renders the Ludo game page """
    return render(request, "ludo.html")
