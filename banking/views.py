
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib import messages

from .forms import SignUpForm


class LandingView(TemplateView):
    template_name = "banking/landing.html"


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "banking/signup.html"
    success_url = reverse_lazy("banking:dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Account created successfully!")
        return response


class BankLoginView(LoginView):
    template_name = "banking/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("banking:dashboard")


@login_required
def dashboard(request):
    accounts = request.user.accounts.all()
    return render(request, "banking/dashboard.html", {"accounts": accounts})