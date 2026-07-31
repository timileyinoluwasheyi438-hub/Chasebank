from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = "banking"

urlpatterns = [
    path("", views.LandingView.as_view(), name="landing"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.BankLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="banking:landing"), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
]