from django.db import models

# Create your models here.
from django.db import models 

class Customer(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank= True, null=True)
    email = models.EmailField(blank=True, null=True)
    document = models.CharField(max_length=30, blank= True, null=True)
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name