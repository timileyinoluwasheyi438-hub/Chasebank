from django.contrib import admin
from .models import Account, CustomerProfile, Transaction

admin.site.register(CustomerProfile)
admin.site.register(Account)
admin.site.register(Transaction)