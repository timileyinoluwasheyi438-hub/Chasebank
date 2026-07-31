from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Account, CustomerProfile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    account_type = forms.ChoiceField(choices=Account.AccountType.choices, initial=Account.AccountType.CHECKING)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "phone_number", "account_type", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            CustomerProfile.objects.create(user=user, phone_number=self.cleaned_data.get("phone_number", ""))
            Account.objects.create(owner=user, account_type=self.cleaned_data["account_type"])
        return user
