from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from .models import User, Listing, Bid, Comment
from .forms import BidForm, ListingForm, CommentForm

def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all(),
    })
def category(request, category):
    
    
    listings = Listing.objects.filter(category = category)
    
    for category_code, category_name in Listing.SHOPPING_CATEGORIES:
        if category_code == category:
            category = category_name


    return render(request, "auctions/category.html",{
        "category": category, 
        "listings": listings,

    })



def listing(request, listing_id):

    try:
        listing = Listing.objects.get(id=listing_id)
        print(listing.title)
        form = BidForm()
        commentForm = CommentForm()
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    print('penis')
    bid = Bid.objects.filter(listing=listing).aggregate(Max('value'))['value__max']
    comments = Comment.objects.filter(listing = listing)
    if (bid == None):
        bid = 0
    if (request.user == listing.user):
        isUser = True
    else:
        isUser = False
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid": bid,
        "form": form,
        "isUser": isUser,
        "commentForm": commentForm,
        "comments": comments
        
    })

def stopListing(reqeuest, listing_id):
    try:
        listing = Listing.objects.get(pk = listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing not found")
    listing.delete()

    return HttpResponseRedirect(reverse("auctions:index"))

@login_required
def bid(request, listing_id):
     if request.method == "POST":

        try:
            print(listing_id)
            print(request.user.id)
            user = User.objects.get(pk = request.user.id)
            #user = request.user //couldnt i just do this lmao 
            listing = Listing.objects.get(pk=listing_id)
            form = BidForm(request.POST)
        except KeyError:
            return HttpResponseBadRequest("Bad Request: no listing chosen")
        except Listing.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: listing does not exist")
        except User.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: user does not exist")
        if form.is_valid():

            bid_amount = form.clean_bid_amount()
            new_bid = Bid(value = bid_amount, user = user, listing = listing )
            new_bid.save()
            if (bid_amount > listing.current_bid):
                listing.current_bid = bid_amount
                return HttpResponseRedirect("/" + str(listing_id))
            else:
                #Want to add functionality to display error message when this happens
                pass

        else:
            return render(request, "auctions/error_handling.html", {
                "code": 400,
                "message": "Form is invalid"
            })

@login_required
def wishlist(request):
    wishlist_items = request.user.wishes.all()
    return render(request, "auctions/wishlist.html",{
        "wishes": wishlist_items
    })

@login_required
def mylistings(request):

    listings = Listing.objects.filter(user = request.user)
    print(listings)
    return render(request, "auctions/mylistings.html",{
        "listings":listings
    })

@login_required
def add_listing(request):
    if request.method == "POST":
        new_listing = Listing.objects.create(title = request.POST["title"], description = request.POST["description"], 
                                             image = request.POST["image"], user = request.user)
        new_listing.save()

        return HttpResponseRedirect(reverse("auctions:index"))
    if request.method == "GET":
        new_listing_form = ListingForm()


        return render(request, "auctions/add_listing.html", {
            "new_listing_form": new_listing_form,
        })

@login_required       
def comment(request, listing_id):
    if request.method == "POST":
        new_comment = Comment.objects.create(user = request.user, listing = Listing.objects.get(pk = listing_id),
                                             comment = request.POST["comment"])
        # to get listing, could also set a related name in comment i think, this would be better if I didnt want to have to
        # pass listing_id, but its fine for now
        new_comment.save()

        return HttpResponseRedirect(reverse("auctions:listing", args=(listing_id,)))




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
    



