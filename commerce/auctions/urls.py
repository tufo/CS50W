from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    # created duplicate paths for category to allow for optional Category parameter.
    # this path is for the categories URL in index.html
    path("categories/", views.categories, name="categories"),
    # this path is for the URLs generated from within categories.html
    path("categories/<str:Category>", views.categories, name="categories"),
    path("listing/<str:listing_id>", views.listing, name="listing")
]
