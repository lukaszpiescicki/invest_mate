from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    ProfileUpdateView,
    UserActivationView,
    UserPortfolioView,
    UserRegisterView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path(
        "accounts/profile/",
        ProfileUpdateView.as_view(template_name="users/profile.html"),
        name="profile",
    ),
    path(
        "portfolio/",
        UserPortfolioView.as_view(template_name="users/portfolio.html"),
        name="portfolio",
    ),
    path(
        "activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        UserActivationView.as_view(),
        name="activate",
    ),
]
