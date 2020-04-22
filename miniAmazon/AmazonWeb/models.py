from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create youur models here.

class Warehouse(models.Model):
    x_location = models.IntegerField()
    y_location = models.IntegerField()

    
class Product(models.Model):
    name = models.CharField(max_length = 200, default = "name")
    description = models.TextField(blank = True)
    price = models.DecimalField(max_digits = 9, decimal_places = 2)


class userprofile(User):
    myaddress_x = models.IntegerField()
    myaddress_y = models.IntegerField()
    
class Order(models.Model):
    #the fields user generate
    create_time = models.DataTimeField()
    dst_x = models.IntegerField()
    dst_y = models.IntegerField()
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #the fields that server generate
    warehouse_id = models.ForeignKey(Warehouse, on_delete = models.CASCADE)
    is_processed = models.BooleanField()
    status = models.TextField(blank = True)
    
class Truck(model.Model):
    truck_id = model.IntegerField()
    warehouse_id = models.ForeignKey(Warehouse)

    
