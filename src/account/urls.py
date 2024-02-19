from django.contrib.auth.views import LogoutView
from django.urls import path

from account.views import user_login, user_signup

app_name = "account"

urlpatterns = [
    path("signup/", user_signup, name="signup"),
    path("login/", user_login, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
