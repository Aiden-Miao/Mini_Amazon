from django.db import models

# Create your models here.
class Warehouse(models.Model):
    wh_id = models.IntegerField()
    x_location = models.IntegerField()
    y_location = models.IntegerField()
    
class Product(models.Model):
    name = models.CharField(max_length = 200, default = "name")
    description = models.CharField(max_length = 1024, default = "Product description")
    count = models.IntegerField()
