from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    cash = models.PositiveIntegerField(default = 0)
    
    
    def __str__(self):
        return self.username
