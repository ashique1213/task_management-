from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('superadmin', 'SuperAdmin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    assigned_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_users')