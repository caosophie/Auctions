from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Bids, User, ActiveListing, ArticleType, Watchlist, Comment
from .forms import CommentForm, CreateForm, BidForm

def index(request):
    user = request.user

    for activelisting in ActiveListing.objects.all():
        print(activelisting)
        print(activelisting.id)
        if Watchlist.objects.filter(user=user, listings=activelisting).exists():
            activelisting.watching = "Remove from watchlist"
        else:
            activelisting.watching = "Add to watchlist"
        
        activelisting.save()

    return render(request, "auctions/index.html", {
        "activelisting" : ActiveListing.objects.all(),
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
def createlisting(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            bid = form.cleaned_data["bid"]
            image_url = form.cleaned_data["image_url"]
            user = request.user
            category = ArticleType.objects.get(type=request.POST["categories"])
            activelisting = ActiveListing.objects.create(user=user, name=title, description=description, bid=bid, image=image_url, category=category)
            Bids.objects.create(user=user, listing=activelisting, price=bid)

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/createlisting.html", {
            "form" : CreateForm(),
            "categories" : ArticleType.objects.all()
        })


def activelisting(request, activelisting_id):
    activelisting = ActiveListing.objects.get(id=activelisting_id)
    user = request.user
    watchlist = Watchlist.objects.filter(user=user)

    # Add to watchlist
    if Watchlist.objects.filter(user=user, listings=activelisting).exists():
        activelisting.watching = "Remove from watchlist"
    else:
        activelisting.watching = "Add to watchlist"
        
    activelisting.save()

    # Post a comment
    if request.method == "POST" and "comm" in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comm = form.cleaned_data["comm"]
            Comment.objects.create(user=user, comment=comm, listing=activelisting)

    # Bid
    if request.method == "POST" and "bid" in request.POST:
        bidform = BidForm(request.POST)
        if bidform.is_valid():
            new_bid = bidform.cleaned_data["bid"]
            if new_bid > activelisting.bid:
                activelisting.bid = new_bid
                Bids.objects.create(user=user, listing=activelisting, price=new_bid)
                activelisting.save()


    # Status 
    status = ""
    if activelisting.status == True:
        status = "Closed"
    else:
        status = "Open"

    # Winner
    message = ""
    if activelisting.status == True and Bids.objects.filter(user=user, listing=activelisting, price=activelisting.bid).exists():
        message = "Congratulations! You've won the auction on this article."

    return render(request, "auctions/listing.html", {
        "activelisting" : activelisting,
        "form" : CommentForm(),
        "comments" : Comment.objects.filter(listing=activelisting),
        "bidform" : BidForm(),
        "status" : status,
        "message" : message
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories" : ArticleType.objects.all()
    })

def ea_category(request, category_id):
    category = ArticleType.objects.get(id=category_id)
    listings = ActiveListing.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "category" : category,
        "listings" : listings
    })

def closingbid(request, activelisting_id):
    user = request.user
    listing = ActiveListing.objects.get(id = activelisting_id)

    if listing.user == user:
        listing.status = True
        listing.save()
        print(listing.status)

    return activelisting(request, activelisting_id)

@login_required
def watching(request, activelisting_id):
    user = request.user
    activelisting = ActiveListing.objects.get(id = activelisting_id)

    if activelisting.watching == "Add to watchlist":
        try:
            watchlist = Watchlist.objects.get(user=user, listings = activelisting_id)
        except:
            watchlist = Watchlist.objects.create(user=user, listings = activelisting)
        return HttpResponseRedirect(reverse("index"))
    else:
        remove(request, activelisting_id)

    return HttpResponseRedirect(reverse("index"))

@login_required
def remove(request, activelisting_id):
    user = request.user
    activelisting = ActiveListing.objects.get(id=activelisting_id)
    
    try:
        watchlist = Watchlist.objects.filter(user=user, listings = activelisting).delete()
    except:
        pass
    
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def watchlist(request):
    user = request.user
    list_id = Watchlist.objects.filter(user=user).values("listings")
    activelisting = ActiveListing.objects.filter(id__in = list_id)
    return render(request, "auctions/watchlist.html", {
        "list_id" : list_id,
        "activelisting" : activelisting
    })