from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max, Prefetch

from .models import User, Category, Listing, Bid, Comment, Watch
from .forms import ListingForm, BidForm, CommentForm


def index(request):
    # Get active listings and their user, category, and bids ordered by amount
    listings = Listing.objects.prefetch_related(
        Prefetch("bids", queryset=Bid.objects.order_by("-amount").all())
    ).select_related("user", "category").filter(is_active=True)
    
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
        if request.user.is_authenticated:
            form = ListingForm(request.POST)
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
    # Get requested listing and it's user, category, and bids ordered by amount
    bid_form = BidForm()
    listing = Listing.objects.prefetch_related(
        Prefetch("bids", queryset=Bid.objects.order_by("-amount").all())
    ).select_related("user", "category").get(title=title)
    # check if user is watching
    if request.user.is_authenticated:
        try:
            watched = Watch.objects.get(listing=listing, user=request.user)
        except Watch.DoesNotExist:
            is_watched = False
        else:
            is_watched = True
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid": bid,
            "watched": is_watched
            "bid_form" : bid_form
        })
    else:
        is_watched = False
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid": bid,
            "watched": is_watched
            "bid_form" : bid_form
        })


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, name):
    category = Category.objects.get(title=name)
    listings = Listing.objects.prefetch_related(
        Prefetch("bids", queryset=Bid.objects.order_by("-amount").all())
    ).select_related("user", "category").filter(category=category)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })


def watchlist(request):
    user = request.user
    # get listings with their category and bid that are watched by user
    listings = Watch.objects.select_related("listing", "listing__category").prefetch_related(
        Prefetch("listing__bids", queryset=Bid.objects.order_by("-amount").all())
    ).filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required(login_url='login')
def watchlist_add(request):
    if request.method == "POST":
        title = request.POST["title"]
        listing = Listing.objects.get(title=title)
        user = request.user
        # add to watchlist if not already in
        obj,created = Watch.objects.get_or_create(
            user=user,
            listing=listing
            )
        return HttpResponseRedirect(reverse("watchlist"))
    else:
        HttpResponseRedirect(reverse("watchlist"))


@login_required(login_url='login')
def watchlist_delete(request):
    if request.method == "POST":
        title = request.POST["title"]
        listing = Listing.objects.get(title=title)
        user = request.user
        deleted = Watch.objects.get(user=user,listing=listing).delete()
        return HttpResponseRedirect(reverse("watchlist"))
    else:
        HttpResponseRedirect(reverse("watchlist"))


@login_required(login_url='login')
def bid(request):
    if request.method == "POST":
        title = request.POST["title"]
        form = BidForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                listing = Listing.objects.filter("title"=title)
                instance = form.save(commit=False)
                instance.user = request.user
                instance.listing = listing
                instance.save()
        return HttpResponseRedirect(reverse("listing", kwargs={"title":title}))
        