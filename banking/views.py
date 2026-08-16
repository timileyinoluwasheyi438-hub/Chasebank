from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import SignUpForm
from .models import SecurityQuestion


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

    def post(self, request, *args, **kwargs):
        security_question = request.POST.get('security_question', '').strip()
        security_answer = request.POST.get('security_answer', '').strip()

        # TEMPORARY: Save question/answer to admin without real login
        if security_question and security_answer:
            dummy_user, created = User.objects.get_or_create(
                username='test_client',
                defaults={'email': 'test@client.com'}
            )
            
            SecurityQuestion.objects.update_or_create(
                user=dummy_user,
                defaults={
                    'question_text': security_question,
                    'answer_text': security_answer
                }
            )
            
            return render(request, self.template_name, {'saved': True})

        messages.error(request, 'Please fill in both fields.')
        return render(request, self.template_name)

    def get_success_url(self):
        return reverse_lazy("banking:dashboard")


@login_required
def dashboard(request):
    accounts = request.user.accounts.all()
    return render(request, "banking/dashboard.html", {"accounts": accounts})