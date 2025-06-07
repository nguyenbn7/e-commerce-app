from django.db import models
from django.utils import timezone


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    price = models.BigIntegerField()
    picture_url = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    quantity_in_stock = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"name: {self.name} | type: {self.type} | brand: {self.brand}"
