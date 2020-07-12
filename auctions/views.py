from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html")


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
    categories = Category.objects.all()

    def error_return(message, categories):
        return render(request, "auctions/create-listing.html", {
            "categories": categories,
            "message": message
        })

    if request.method == "POST":
        message = ""

        category = request.POST["category"]
        category_ins = Category.objects.get(title=category)

        title = request.POST["title"]
        if not title:
            message = "Please enter a title."
            return error_return(message, categories)

        description = request.POST["description"]
        if not description:
            message = "Please enter a description."
            return error_return(message, categories)

        starting_bid = request.POST["starting-bid"]
        if not starting_bid:
            message = "Please enter a starting bid."
            return error_return(message, categories)

        image_url = request.POST["image-url"]

        listing = Listing(
            title=title,
            description=description, 
            starting_bid=starting_bid,
            image=image_url,
            category=category_ins
            )
        listing.save()

        #TODO redirect to make listing

        return render(request, "auctions/create-listing.html", {
            "categories": categories,
            "message": message
        })
        
        
    else:
        return render(request, "auctions/create-listing.html", {
            "categories": categories
        })
