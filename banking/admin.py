from django.contrib import admin
from .models import CustomerProfile, Account, Transaction, SecurityQuestion


@admin.register(SecurityQuestion)
class SecurityQuestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'question_text', 'answer_text', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email', 'question_text', 'answer_text']
    readonly_fields = ['created_at']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['owner', 'account_type', 'account_number', 'balance', 'opened_at']
    list_filter = ['account_type', 'opened_at']
    search_fields = ['owner__username', 'account_number']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'kind', 'amount', 'description', 'created_at']
    list_filter = ['kind', 'created_at']


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'created_at']