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
    listings = Listing.objects.annotate(
        max_bid=Max('bids', filter=Q(is_active=True))
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


@login_required(login_url='login')
def create_listing(request):
    form = ListingForm()
    if request.method == "POST":
        #form = ListingForm(request.POST)
        if request.user.is_authenticated:
            form = ListingForm(request.POST)
            #form.user = request.user
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                title = request.POST["title"]
                return HttpResponseRedirect(reverse("listing", kwargs={"title":title}))
    return render(request, "auctions/create-listing.html", {
        "form": form
    })


def listing(request, title):
    listing = Listing.objects.select_related('user').get(title=title)
    return render(request, "auctions/listing.html", {
        "listing": listing
    })


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, name):
    category = Category.objects.get(title=name)
    listings = category.listings.annotate(
        max_bid=Max('bids', filter=Q(is_active=True))
    )
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })