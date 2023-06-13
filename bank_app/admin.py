from django.contrib import admin
from .models import Transaction
# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "amount", "description", "customer")
    list_filter = ("customer", "date")

admin.site.register(Transaction, TransactionAdmin)
