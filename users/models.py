from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    user_type = models.CharField(
        max_length=10, choices=[('customer', 'Customer'), ('admin', 'Admin')],
        default='customer' 
    )

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['first_name', 'last_name']  
    def save(self, *args, **kwargs):
        
        if not self.username:
            self.username = f"user_{self.email.split('@')[0]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email 
