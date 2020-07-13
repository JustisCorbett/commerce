from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max

from .models import User, Category, Listing, Bid, Comment, Watch
from .forms import ListingForm, BidForm, CommentForm


def index(request):
    #listings = Listing.objects.filter(is_active=True).annotate(models.Max(Bid))
    listings = Listing.objects.annotate(
        max_bid=Max('bid', filter=Q(is_active=True))
    )
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    form = ListingForm

    def error_return(message, categories):
        return render(request, "auctions/create-listing.html", {
            "form": form,
            "message": message
        })

    if request.method == "POST":
        

        return render(request, "auctions/create-listing.html", {
            "form": form,
            "message": message
        })
        
        
    else:
        return render(request, "auctions/create-listing.html", {
            "form": form,
        })
