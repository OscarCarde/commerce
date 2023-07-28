from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max, Count
from math import floor
from decimal import *

from .models import *
from .forms import *

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active = True)
    })

def sell(request):

    if request.user.is_authenticated:
        if request.method == "POST":

            item = ListingForm(request.POST, request.FILES)

            if item.is_valid:
                listing = item.save(commit=False)
                listing.seller = request.user
                listing.save()
            

            return render(request, "auctions/sell.html", {
            "form": ListingForm()
            })
        return render(request, "auctions/sell.html", {
        "form": ListingForm()
        })

    else:
        return render(request, "auctions/login.html")

def watchlist(request):
    if request.user.is_authenticated:

        return render(request, "auctions/watchlist.html", {
            "watched": request.user.watchlist.all()
        })

    return HttpResponseRedirect("register")

def listing(request, listing_id):

    listing = Listing.objects.get(id = listing_id)
    max_bid = listing.max_bid if listing.max_bid > 0 else listing.price
    invalid_bid = False

        #implement bid form
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect("register")

        if "place-bid" in request.POST:
            a_bid = Decimal(request.POST["bid"])
            
            if a_bid > max_bid:
                new_bid = BidForm(request.POST)
                bid = new_bid.save(commit=False)          
                bid.bider = request.user
                bid.item = Listing.objects.get(id=listing_id)
                bid.save()
            else:
                invalid_bid = True

        elif "watchlist" in request.POST:
                is_watching = listing in request.user.watchlist.all()

                if is_watching:
                    request.user.watchlist.remove(listing)
                else:
                    request.user.watchlist.add(listing)
        elif "close-auction" in request.POST:
            listing.close_auction()
            return HttpResponseRedirect(listing_id)
        
        elif "commenting" in request.POST:
            new_comment = CommentForm(request.POST)
            comment = new_comment.save(commit=False)
            comment.commenter = request.user
            comment.listing = listing
            comment.save()

    listing = Listing.objects.get(id = listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing, "form": BidForm(), 
        "watched": listing in request.user.watchlist.all(), 
        "invalid_bid": invalid_bid, "comment_form": CommentForm()
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

