from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=200, unique = True)
    email_domain = models.CharField(max_length=100, unique = True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('staff', 'Staff'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default = 'customer')
    is_verified_student = models.BooleanField(default=False)
    university = models.ForeignKey(
        University, 
        on_delete=models.SET_NULL, 
        null=True, blank = True
    )
    def __str__(self):
        return self.username