from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.db.models import F
from .models import TicTacToeLeaderboard, RPSLeaderboard, MemoryLeaderboard, GameReview, SnakeLeaderboard, LudoMatchLeaderboard
from django.utils.timezone import now

import random
import json


# -------------------- HOME & BASIC PAGES --------------------

def home(request):
    """ Render the home page with leaderboards. """
    tic_tac_toe_leaderboard = sorted(
    TicTacToeLeaderboard.objects.all(),
    key=lambda player: player.wins - player.losses,  # Calculate final_score manually
    reverse=True
)[:10]

    rps_leaderboard = sorted(
    RPSLeaderboard.objects.all(),
    key=lambda player: player.wins - player.losses,
    reverse=True
)[:10]

    memory_leaderboard = sorted(
    MemoryLeaderboard.objects.all(),
    key=lambda player: player.time_taken  # Lower time is better
)[:10]

    snake_leaderboard = sorted(
    SnakeLeaderboard.objects.all(),
    key=lambda player: player.score,
    reverse=True
)[:10]


    return render(request, 'home.html', {
        'tic_tac_toe_leaderboard': tic_tac_toe_leaderboard,
        'rps_leaderboard': rps_leaderboard,
        'memory_leaderboard': memory_leaderboard,
        'snake_leaderboard': snake_leaderboard
    })


def about(request):
    """ Render the About page. """
    return render(request, 'about.html')

# -------------------- Game Pages --------------------

@login_required
def tic_tac_toe(request):
    """ Render the Tic Tac Toe game page. """
    return render(request, "tic_tac_toe.html")

@login_required
def rock_paper_scissors(request):
    """ Render the Rock Paper Scissors game page. """
    return render(request, 'rock_paper_scissors.html')

@login_required
def memory_card_game(request):
    """ Render the Memory Card Game page. """
    return render(request, "memory_card_game.html")

@login_required
def snake_game(request):
    return render(request, "snake_game.html")

@login_required
def chess_game(request):
    return render(request, "chess.html")

@login_required
def ludo_game(request):
    """ Renders the Ludo game page """
    return render(request, "ludo.html")

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


# -------------------- ROCK PAPER SCISSORS - Game Play --------------------

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


# -------------------- SCORE & LEADERBOARD --------------------

@login_required
def memory_leaderboard(request):
    """ Fetch and display the Memory Card Game leaderboard. """
    leaderboard = MemoryLeaderboard.objects.order_by("time_taken")[:10]  # Lowest time is better
    return render(request, "memory_leaderboard.html", {"leaderboard": leaderboard})

@login_required
def snake_leaderboard(request):
    """ Fetch and display the Snakex game leaderboard. """
    leaderboard = SnakeLeaderboard.objects.order_by("-score")[:10]  # Highest score first
    return render(request, "snake_leaderboard.html", {"leaderboard": leaderboard})

@login_required
def rock_paper_scissors_leaderboard(request):
    """ Render the Rock Paper Scissors leaderboard page. """
    leaderboard = RPSLeaderboard.objects.order_by('-final_score', '-wins')[:10]  # Top 10 players sorted by score

    return render(request, 'rock_paper_scissors_leaderboard.html', {
        "leaderboard": leaderboard
    })

# -------------------- TIC-TAC-TOE LEADERBOARD --------------------

@login_required
def get_tic_tac_toe_leaderboard(request):
    """ API to fetch Tic-Tac-Toe leaderboard dynamically. """
    leaderboard_data = TicTacToeLeaderboard.objects.order_by('-wins', 'losses')[:10]
    leaderboard = [
        {
            "rank": index + 1,
            "user": entry.user.username,
            "wins": entry.wins,
            "losses": entry.losses,
            "final_score": entry.final_score,
        }
        for index, entry in enumerate(leaderboard_data)
    ]
    return JsonResponse({"leaderboard": leaderboard})


@login_required
@csrf_exempt
def update_tic_tac_toe_score(request):
    """ Update Tic-Tac-Toe Leaderboard """
    if request.method == "POST":
        data = json.loads(request.body)
        result = data.get("result")  # 'win', 'loss', 'draw'
        user = request.user

        leaderboard_entry, _ = TicTacToeLeaderboard.objects.get_or_create(user=user)

        if result == "win":
            leaderboard_entry.wins += 1
        elif result == "loss":
            leaderboard_entry.losses += 1
        elif result == "draw":
            leaderboard_entry.draws += 1

        leaderboard_entry.save()

        return JsonResponse({"message": "Score updated successfully!"})

    return JsonResponse({"error": "Invalid request"}, status=400)


# -------------------- ROCK-PAPER-SCISSORS LEADERBOARD --------------------

from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def update_rps_score(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            result = data.get("result")

            # Debugging: Check if data is received
            print("Received data:", data)

            if result == "win":
                request.user.profile.rps_wins += 1
            elif result == "lose":
                request.user.profile.rps_losses += 1

            request.user.profile.save()
            return JsonResponse({"message": "Score updated successfully"})
        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def get_rps_leaderboard(request):
    """ API to fetch Rock Paper Scissors leaderboard. """
    leaderboard_data = RPSLeaderboard.objects.all()

    leaderboard = sorted(
        leaderboard_data,
        key=lambda x: (x.wins - x.losses, x.wins),
        reverse=True
    )[:10]  # Sort by computed final score and then wins

    leaderboard_response = [
        {
            "rank": index + 1,
            "player": entry.user.username,
            "wins": entry.wins,
            "losses": entry.losses,
            "draws": entry.draws,
            "final_score": entry.wins - entry.losses,  # Compute score dynamically
        }
        for index, entry in enumerate(leaderboard)
    ]

    return JsonResponse({"leaderboard": leaderboard_response})


# -------------------- MEMORY CARD GAME LEADERBOARD --------------------

@login_required
def get_memory_leaderboard(request):
    """ API to fetch Memory Card Game leaderboard dynamically. """
    leaderboard_data = MemoryLeaderboard.objects.order_by("time_taken")[:10]  # Rank by least time
    leaderboard = [
        {
            "rank": index + 1,
            "user": entry.user.username,
            "time_taken": entry.time_taken
        }
        for index, entry in enumerate(leaderboard_data)
    ]
    return JsonResponse({"leaderboard": leaderboard})

@login_required
def update_memory_score(request):
    """ API to update Memory Card Game scores. """
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        time_taken = data.get("time_taken")

        if not isinstance(time_taken, (int, float)) or time_taken <= 0:
            return JsonResponse({"status": "error", "message": "Invalid time"}, status=400)

        entry, _ = MemoryLeaderboard.objects.get_or_create(user=user)
        if time_taken < entry.time_taken:  # Only update if the new time is lower
            entry.time_taken = time_taken
            entry.save()

        return JsonResponse({"status": "success", "new_time": entry.time_taken})
    
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

# -------------------- SNAKE GAME LEADERBOARD --------------------

@login_required
def get_snake_leaderboard(request):
    """API to fetch Snake leaderboard."""
    leaderboard_data = SnakeLeaderboard.objects.order_by("-score")[:10]
    leaderboard = [
        {
            "rank": index + 1,
            "player": entry.user.username,
            "score": entry.score,
        }
        for index, entry in enumerate(leaderboard_data)
    ]
    return JsonResponse({"leaderboard": leaderboard})


@login_required
def update_snake_score(request):
    """API to update Snake Game leaderboard."""
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        score = data.get("score")

        if not isinstance(score, int) or score < 0:
            return JsonResponse({"status": "error", "message": "Invalid score"}, status=400)

        entry, _ = SnakeLeaderboard.objects.get_or_create(user=user)
        if score > entry.score:  # Only update if the new score is higher
            entry.score = score
            entry.save()

        return JsonResponse({"status": "success", "new_score": entry.score})
    
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

# -------------------- LUDO LEADERBOARD (PER GAME) --------------------

@login_required
def update_ludo_leaderboard(request):
    """ Updates the Ludo leaderboard for a single match (resets after each game). """
    if request.method == "POST":
        data = json.loads(request.body)
        leaderboard_entries = data.get("leaderboard", [])  # Expected [{user, score}]

        # Clear old data (since Ludo leaderboard resets every match)
        LudoMatchLeaderboard.objects.all().delete()

        for entry in leaderboard_entries:
            LudoMatchLeaderboard.objects.create(user=entry["user"], score=entry["score"])  # ✅ Changed `player` to `user`

        return JsonResponse({"status": "success", "message": "Ludo leaderboard updated!"})


@login_required
def get_ludo_leaderboard(request):
    """ Fetches the temporary Ludo leaderboard for the current match. """
    leaderboard = LudoMatchLeaderboard.objects.order_by('-score')
    leaderboard_data = [{"user": entry.user.username, "score": entry.score} for entry in leaderboard]  # ✅ Changed `player` to `user`
    return JsonResponse({"leaderboard": leaderboard_data})


# -------------------- GAME REVIEW --------------------

@login_required
def submit_review(request):
    """ Allows users to submit game reviews. """
    if request.method == "POST":
        data = json.loads(request.body)
        game_name = data.get("game_name")
        review_text = data.get("review_text")

        if not game_name or not review_text:
            return JsonResponse({"status": "error", "message": "Missing game name or review text"}, status=400)

        GameReview.objects.create(user=request.user, game_name=game_name, review_text=review_text)
        return JsonResponse({"status": "success", "message": "Review submitted!"})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

#---------------------- Chess Game ---------------------
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


