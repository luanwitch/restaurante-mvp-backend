from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    document = models.CharField(max_length=30, blank = True, null=True)
    category = models.CharField(max_length=80, blank=True, null= True)
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name