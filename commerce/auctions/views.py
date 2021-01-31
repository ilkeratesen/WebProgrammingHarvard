from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Textarea
from .models import User,Listings, Bids, Comments
from .forms import NewListingForm, BidsForm
from django import forms
from django.shortcuts import get_object_or_404
from django.contrib import messages



def index(request):
    
    return render(request, "auctions/index.html", {
        'listings': Listings.objects.filter(active=False)
    })

def all_listings(request):
    
    return render(request, "auctions/all.html", {
        'listings': Listings.objects.all()
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
def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        try:
            new_listing = form.save(commit=False)
            assert request.user.is_authenticated
            new_listing.auction_owner = request.user
            new_listing.save()
           
            return HttpResponseRedirect(reverse("index"))

        except ValueError:
            pass

    else:
        form = NewListingForm()
    return render(request, "auctions/create.html", {
        "form": form
    })

@login_required
def create_bid(request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        bid = Bids(user=request.user, listing=listing)
        bid_form = BidsForm(request.POST, instance=bid)
        if bid_form.is_valid():
            bid_form.save()
        else:
            return listing_page(request, listing_id, bid_form=bid_form)

    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))

def listing_page(request, listing_id, bid_form=None):
    listing = Listings.objects.get(pk=listing_id)
    print(listing.active)
    if request.user.is_authenticated:
        watchlisted = request.user.watchlist_items.filter(pk=listing_id).exists()

        if not bid_form:
            bid_form = BidsForm()
            
        owned = listing.auction_owner == request.user
    else:
        watchlisted = None
        owned = None
        bid_form = None
    return render(request, "auctions/listing.html", {
        'listing': listing,
        'form': bid_form,
        'watchlisted': watchlisted,
        'owned': owned
    })

@login_required
def active_listings(request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        print(request.user)
        print(listing.auction_owner)
        print(listing.auction_owner == request.user)
        if request.user == listing.auction_owner:
            listing.active = True
            listing.save()
    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))

@login_required
def commenting(request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        comment_content = request.POST['comment']
        comment = Comments(commenter=request.user, listing=listing, content=comment_content)
        comment.save()
    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))

@login_required
def watchlist(request, listing_id):
    if request.method == "POST":
        assert request.user.is_authenticated
        user = request.user
        listing = Listings.objects.get(pk=listing_id)
        if user.watchlist_items.filter(pk=listing_id).exists():
            user.watchlist_items.remove(listing)
        else:
            user.watchlist_items.add(listing)

    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))

@login_required
def watchlist_page(request):
    assert request.user.is_authenticated
    return render(request, "auctions/watchlist.html", {
        'listings': request.user.watchlist_items.all()
        
    })

def filtered_categories(request, category):
    return render(request, "auctions/index.html", {
        'listings': Listings.objects.filter(active=False, category=category),
        'title': f'Active listings under "{category}"'
    })
    
def category_page(request):
    categories = list(set([listing.category for listing in Listings.objects.all() if listing.category]))
    print(categories)
    return render(request, "auctions/categories.html", {
        'categories': categories
    })
