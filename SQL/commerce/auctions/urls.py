from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_Listing, name="create_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("bid/new", views.new_bid, name="new_bid"),
    path("add/watchlist", views.add_to_watchlist, name="addwatchlist"),
    path("user/profile", views.user_profile, name="user_watchlist"),
    path("show/category", views.show_category, name="show_category"),
    path("remove", views.remove_from_watchlist, name="removewatchlist"),
    path("comment", views.add_comment, name="addcomment"),
    path("closelisting", views.close_listing, name="closelisting"),
    path("all_listings", views.all_listings, name="all_li")
]
    
