from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("sell", views.sell, name = "sell"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("listing/<str:listing_id>", views.listing, name = "listing"),
    path("categories", views.categories, name="categories"),
    path("<str:category>", views.index, name="index")
]
