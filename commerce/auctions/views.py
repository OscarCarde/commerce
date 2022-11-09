from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max, Count
from django import forms
from math import floor

from .models import *

class NewListing(forms.Form):
    title = forms.CharField(max_length = 90, label='Title', widget = forms.TextInput(attrs={'class': ''}))
    description = forms.CharField(max_length = 500, label='Enter your item\'s description here',widget = forms.Textarea(attrs={'class':'my-5'}))
    asking_price = forms.DecimalField(max_digits = 11, decimal_places = 2, label='Price')
    image = forms.ImageField()

def index(request):
    listings = Listing.objects.annotate(max_bid = Max('bids__bid'), item_bids = Count('bids'))
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

def sell(request):

    if request.user.is_authenticated:
        if request.method == "POST":

            title = request.POST["title"]
            description = request.POST["description"]
            price = request.POST["asking_price"]
            image = request.POST["image"]

            listing = Listing(item = title, description = description, price = price, image = image, seller = request.user)
            listing.save()

            return render(request, "auctions/sell.html", {
            "form": NewListing()
            })
        return render(request, "auctions/sell.html", {
        "form": NewListing()
        })

    else:
        return render(request, "auctions/login.html")

def listing(request, listing_id):

    listings = Listing.objects.annotate(max_bid = Max('bids__bid'), bids_count = Count('bids'))
    listing = listings.get(id = listing_id)
    max_bid = listing.max_bid
    if max_bid != None:
        max_bid = round(max_bid, 2)

    return render(request, "auctions/listing.html", {
        "listing": listing, "max_bid": max_bid
    })
