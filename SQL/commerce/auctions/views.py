from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    
    
    listing_entries = Listing.objects.filter(isActive=True)
    categories = Category.objects.all()
    #listing_items = [item.product for item in listing_entries]
    if list(listing_entries) != [] :
        return render(request, "auctions/index.html", {
            #"listing_items":listing_items,
            "listing_entries":listing_entries,
            "categories":categories
        })
    else:
        return render(request, "auctions/index.html", {
            "message": "Currently no listings",
            "categories":categories
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
#Seems like its neccesary only the current_bid
def create_Listing(request):
    categories = Category.objects.all()
    if request.method == "POST":
        current_user = request.user
        if current_user.is_authenticated:
            
            item = request.POST["item"]
            description = request.POST["description"]
            price = float(request.POST["price"])
            bid = Bid(user_bid = current_user, new_bid=price)
            bid.save()
            cat = request.POST["category"]
            category = Category.objects.get(category = cat)
            listing = Listing(product = item, description = description, minimum_bid = bid, user_owner = current_user, category=category, isActive=True)
            listing.save()
            
            return render(request, "auctions/listing.html", {
            
                "product": listing.product,
                "description": listing.description,
                "price": listing.minimum_bid
         })
    return render(request, "auctions/create_listing.html", {
        "Categories": categories
    })



def listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk = listing_id)
        allComments = listing.comment.all()
        user = request.user

        if user.is_authenticated:
            if user == listing.user_owner:
                if listing in user.user_watchlist.all():
                    is_in_watchlist = True
                    return render(request, "auctions/listing.html", {
                        "thelist":listing.isActive,
                        "listing": listing.pk,
                        "product": listing.product,
                        "description": listing.description,
                        "price": listing.minimum_bid,
                        "is_in_watchlist":is_in_watchlist,
                        "allComments": allComments,
                        "userisOwner":True,
                        "user":user
                })
            
                else: 
                    is_in_watchlist = False
                    return render(request, "auctions/listing.html", {
                        "thelist":listing.isActive,
                        "user":user,
                        "userisOwner":True,
                        "listing": listing.pk,
                        "product": listing.product,
                        "description": listing.description,
                        "price": listing.minimum_bid,
                        "is_in_watchlist":is_in_watchlist,
                        "allComments": allComments
                })
            else:
                if listing in user.user_watchlist.all():
                    is_in_watchlist = True
                    return render(request, "auctions/listing.html", {
                        "thelist":listing.isActive,
                        "user":user,
                        "listing": listing.pk,
                        "product": listing.product,
                        "description": listing.description,
                        "price": listing.minimum_bid,
                        "is_in_watchlist":is_in_watchlist,
                        "allComments": allComments,
                        "userisOwner":False
                })
            
                else: 
                    is_in_watchlist = False
                    return render(request, "auctions/listing.html", {
                        "user":user,
                        "thelist":listing.isActive,
                        "userisOwner":False,
                        "listing": listing.pk,
                        "product": listing.product,
                        "description": listing.description,
                        "price": listing.minimum_bid,
                        "is_in_watchlist":is_in_watchlist,
                        "allComments": allComments
                })
                
        
        
        else:
            return render(request, "auctions/listing.html", {
                    "listing": listing.pk,
                    "product": listing.product,
                    "description": listing.description,
                    "price": listing.minimum_bid,
            })
    except:
        return render(request, "auctions/error.html", {
            "message": "Something went wrong. The page you are looking for might not exist"
        })
                
        


def new_bid(request):
    user = request.user
    if user.is_authenticated:
        listing_entries = Listing.objects.all()
        if request.method == "POST":
            bid = float(request.POST["bid"])
            id = int(request.POST["pk"])
            listing = Listing.objects.get(pk = id)  
            if bid > float(listing.minimum_bid.new_bid):
                listing.minimum_bid = Bid(user_bid = user, new_bid = bid)
                listing.minimum_bid.save()
                listing.user_bids.add(user)
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
            else:
                 return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    else:
        pass

def add_to_watchlist(request):
    user = request.user
    if user.is_authenticated:
        listing_entries = Listing.objects.all()
        if request.method == "POST":
           
            id = int(request.POST["pk"])
            listing = Listing.objects.get(pk = id) 
            listing.user_watchlist.add(user) 
            is_in_watchlist = True
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        else:
            return render(request, "auctions/index.html",{
                "listing_entries":listing_entries
            })
    else:
        pass
#maybe do it more  general so that it displays all the thinga related to the user
def user_profile(request):
    user = request.user
    if user.is_authenticated:
        user_watchlist = Listing.objects.filter(user_watchlist = user)
        if user_watchlist:
            return render(request, "auctions/user_watchlist.html", {
                "user_watchlist": user_watchlist
            })
        else:
            return render(request, "auctions/user_watchlist.html", {
                "user_watchlist": user_watchlist,
                "message": "You have no listings in your watchlist"
            })
 
def show_category(request):
    if request.method == "POST":
        if list(Category.objects.all()) != []:
            cat = request.POST["category"]
            category = Category.objects.get(category=cat)
            listing_entries = Listing.objects.filter(isActive=True, category=category)
            categories = Category.objects.all()
            #listing_items = [item.product for item in listing_entries]
            if listing_entries != []:
                return render(request, "auctions/show_category.html", {
                    #"listing_items":listing_items,
                    "listing_entries":listing_entries,
                    "categories":categories
            })
            else:
                    return render(request, "auctions/show_category.html", {
                    "message": "Currently no listings"
                })
           
        else:
            return HttpResponseRedirect(reverse("index"))


def remove_from_watchlist(request):
    user = request.user
    if user.is_authenticated:
        
        if request.method == "POST":
            id = int(request.POST["pk"])
            listing = Listing.objects.get(pk = id) 
            listing.user_watchlist.remove(user)
            is_in_watchlist = False
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
           
    
    else:
        pass
def add_comment(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            id = int(request.POST["pk"])
            listing = Listing.objects.get(pk = id)
            comentario = request.POST["comment"]
            comment = Comment(comment = comentario, listing = listing, user = user)
            comment.save()
            if listing in user.user_watchlist.all():
                is_in_watchlist = True
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

            else:
                is_in_watchlist = False
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        else:
            pass
    else:
        return render(request, "auctions/login.html", {
            "message": "Log in to place a comment"
        })


def close_listing(request):
    if request.method == "POST":
        user = request.user
        id = int(request.POST['pk'])
        listing = Listing.objects.get(pk = id)
        if user == listing.user_owner:
            listing.isActive = False
            listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def all_listings(request):
    
    
    listing_entries = Listing.objects.all()
    categories = Category.objects.all()
    #listing_items = [item.product for item in listing_entries]
    if list(listing_entries) != [] :
        return render(request, "auctions/index.html", {
            #"listing_items":listing_items,
            "listing_entries":listing_entries,
            "categories":categories
        })
    else:
        return render(request, "auctions/index.html", {
            "message": "Currently no listings",
            "categories":categories
        })