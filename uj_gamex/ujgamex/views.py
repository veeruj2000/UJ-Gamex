from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import GameScore, Review, Score, Leaderboard

def home(request):
    scores = GameScore.objects.order_by("-score")[:5]  # Fetch top 5 scores
    reviews = Review.objects.all()  # Fetch all reviews
    leaderboard = Leaderboard.objects.all().order_by('-wins', 'losses')  # Sort by highest wins, then lowest losses
    return render(request, "home.html", {"scores": scores, "reviews": reviews, "leaderboard": leaderboard})

def about(request):
    return render(request, 'about.html')

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

@login_required
def tic_tac_toe(request):
    return render(request, "tic_tac_toe.html")

@login_required
def update_score(request):
    if request.method == "POST":
        result = request.POST.get("result")  # win, loss, or draw
        user = request.user

        # ✅ Update Score Model
        user_score, _ = Score.objects.get_or_create(user=user)

        if result == "win":
            user_score.wins += 1
        elif result == "loss":
            user_score.losses += 1
        elif result == "draw":
            user_score.draws += 1
        else:
            return JsonResponse({"status": "error", "message": "Invalid result"}, status=400)

        user_score.save()

        # ✅ Update Leaderboard Model
        leaderboard_entry, created = Leaderboard.objects.get_or_create(user=user)

        if result == "win":
            Leaderboard.objects.filter(user=user).update(wins=F('wins') + 1)
        elif result == "loss":
            Leaderboard.objects.filter(user=user).update(losses=F('losses') + 1)

        return JsonResponse({
            "status": "success",
            "wins": user_score.wins,
            "losses": user_score.losses,
            "draws": user_score.draws
        })

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@login_required
def update_leaderboard(request, result):
    user = request.user

    leaderboard_entry, _ = Leaderboard.objects.get_or_create(user=user)

    if result == "win":
        Leaderboard.objects.filter(user=user).update(wins=F('wins') + 1)
    elif result == "loss":
        Leaderboard.objects.filter(user=user).update(losses=F('losses') + 1)
    else:
        return JsonResponse({"status": "error", "message": "Invalid result"}, status=400)

    return JsonResponse({"status": "success", "message": "Leaderboard updated"})

def leaderboard_view(request):
    # ✅ Fetch players sorted by final score (wins - losses)
    leaderboard = Leaderboard.objects.all().order_by('-wins', 'losses')
    return render(request, "leaderboard.html", {"leaderboard": leaderboard})
