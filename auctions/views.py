from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max

from .models import User, Category, Listing, Bid, Comment, Watch
from .forms import ListingForm, CommentForm


def index(request):
    listings = Listing.objects.annotate(
        max_bid=Max("bids", filter=Q(is_active=True))
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
    listing = Listing.objects.select_related("user").get(title=title)
    bids = Bid.objects.prefetch_related(
        Prefetch('', queryset=Book.objects.filter(price__range=(250, 300)))
    )
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
            "watched": is_watched
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


def watchlist(request):
    user = request.user
    listings = Watch.objects.select_related('listing').filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required(login_url='login')
def watchlist_add(request):
    if request.method == "POST":
        title = request.POST["title"]
        listing = Listing.objects.get(title=title)
        user = request.user

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
        bid = request.POST["bid"]
        title = request.POST["title"]
        listing = Listing.objects.get(title=title)
        user = request.user

        bid = Bid.objects.create(
            amount=int(bid),
            listing=listing,
            user=user
            )
        