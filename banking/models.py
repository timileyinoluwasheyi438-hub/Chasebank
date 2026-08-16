import random
import string
from django.db import models
from django.contrib.auth.models import User


def generate_account_number():
    return "".join(random.choices(string.digits, k=10))


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile: {self.user.get_username()}"


class Account(models.Model):
    class AccountType(models.TextChoices):
        CHECKING = "checking", "Everyday Checking"
        SAVINGS = "savings", "Growth Savings"

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    account_number = models.CharField(max_length=10, unique=True, default=generate_account_number, editable=False)
    account_type = models.CharField(max_length=20, choices=AccountType.choices)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    opened_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_account_type_display()} ****{self.account_number[-4:]}"


class Transaction(models.Model):
    class Kind(models.TextChoices):
        DEPOSIT = "deposit", "Deposit"
        WITHDRAWAL = "withdrawal", "Withdrawal"
        TRANSFER = "transfer", "Transfer"

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    kind = models.CharField(max_length=20, choices=Kind.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class SecurityQuestion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='security_question')
    question_text = models.CharField(max_length=255)
    answer_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Security Q for {self.user.username}"

    class Meta:
        verbose_name = "Security Question"
        verbose_name_plural = "Security Questions"
