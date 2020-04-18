from django.db import models

# Create your models here.
class Warehouse(models.Model):
    x_location = models.IntegerField()
    y_location = models.IntegerField()
    
