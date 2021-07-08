from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("createlisting/", views.createlisting, name="createlisting"),
    path("activelisting/<str:activelisting_id>", views.activelisting, name="activelisting"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category_id>", views.ea_category, name="ea_category"),
    path("watching/<str:activelisting_id>", views.watching, name="watching"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("removewatching/<str:activelisting_id>", views.remove, name="remove"),
    path("closingbid/<str:activelisting_id>", views.closingbid, name="closingbid")
]
