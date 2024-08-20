from django.urls import path
from django.contrib.auth.views import LoginView

from .views import (
    AboutMeView,
    RegisterView,
    MyLogoutView,
    ProfileUpdateView,
    UserDeleteView,
)

app_name = "myauth"

urlpatterns = [
    path("login/", LoginView.as_view(template_name="myauth/login.html", redirect_authenticated_user=True,), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("register/", RegisterView.as_view(), name="register"),
    path("about-me/<int:pk>/delete/", UserDeleteView.as_view(), name="profile_delete"),
    path("about-me/<int:pk>/update/", ProfileUpdateView.as_view(), name="profile_update"),
]
