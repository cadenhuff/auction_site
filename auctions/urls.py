from django.urls import path

from . import views


app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("wishlist", views.wishlist, name = "wishlist"),
    path("mylistings", views.mylistings, name = "mylistings"),
    path("add_listing", views.add_listing, name = "add_listing"),
    path("<int:listing_id>", views.listing, name = "listing"),
    path("<int:listing_id>/bid", views.bid, name = "bid"),
    path("<int:listing_id>/comment", views.comment, name = "comment"),
    path("<int:listing_id>/stopListing", views.stopListing, name = "stopListing")
    
]
