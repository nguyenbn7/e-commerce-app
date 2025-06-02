from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.BigIntegerField()
    picture_url = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    quantity_in_stock = models.IntegerField()
