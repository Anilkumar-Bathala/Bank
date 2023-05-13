from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=10, unique=True)
    bank = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('withdraw', 'Withdraw'),
        ('deposit', 'Deposit'),
        ('transfer', 'Transfer'),
    )

    TRANSACTION_MODES = (
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    reference_id = models.CharField(max_length=10)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    mode = models.CharField(max_length=10, choices=TRANSACTION_MODES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.reference_id
