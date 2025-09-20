from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """A model for the various users."""
    role_choices = [
        ('admin', 'Admin'),
        ('stock manager', 'Stock Manager'),
        ('agent', 'Agent')
    ]
    middle_name = models.CharField(max_length=250, null=True)
    phone_number  = models.CharField(max_length=15, unique=True, null=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=role_choices, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(upload_to='user/', null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return f'{self. first_name} {self.last_name}'