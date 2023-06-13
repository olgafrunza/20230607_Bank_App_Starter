from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Transaction(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date} {self.amount}"
    
    