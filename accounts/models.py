from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) 
    ROLE_CHOICES = [
        ('usuario', 'Usuario'),
        ('admin', 'Administrador'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='usuario')

    

    def __str__(self):
        return f"{self.username} ({self.role})"