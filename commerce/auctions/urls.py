from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all_listings", views.all_listings, name="all_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing_page/<int:listing_id>", views.listing_page, name="listing_page"),
    path("create_bid/<int:listing_id>", views.create_bid, name="create_bid"),
    path("active_listings/<int:listing_id>", views.active_listings, name="active_listings"),
    path("commenting/<int:listing_id>", views.commenting, name="commenting"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("watchlist_page", views.watchlist_page, name="watchlist_page"),
    path("categories/<str:category>", views.filtered_categories, name='filtered_categories'),
    path("categories", views.category_page, name="categories")
]
