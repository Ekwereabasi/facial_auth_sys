
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change the related_name to avoid conflicts
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Change the related_name to avoid conflicts
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

    def __str__(self):
        return self.username

class Account(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_type = models.CharField(max_length=50, default='Savings')  # Add this line


    def __str__(self):
        return f"{self.user.username}'s Account"

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw'), ('transfer', 'Transfer')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=225, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transaction_type.capitalize()} of ${self.amount} on {self.timestamp}"
