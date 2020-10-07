from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("listing/<str:title>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("category/<str:name>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist-add", views.watchlist_add, name="watchlist_add"),
    path("watchlist-delete", views.watchlist_delete, name="watchlist_delete"),
    path("close_listing", views.close_listing, name="close_listing"),
    path("create_comment", views.create_comment, name="create_comment")
]