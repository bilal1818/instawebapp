from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """Custom user model with role-based access"""
    
    ROLE_CHOICES = (
        ('creator', 'Creator'),
        ('consumer', 'Consumer'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='consumer')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_creator(self):
        return self.role == 'creator'
    
    @property
    def is_consumer(self):
        return self.role == 'consumer'
