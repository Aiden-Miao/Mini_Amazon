from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create youur models here.

class Product(models.Model):
    name = models.CharField(max_length = 200, default = "name")
    description = models.TextField(blank = True)
    price = models.DecimalField(max_digits = 9, decimal_places = 2)

class WhInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Warehouse(models.Model):
    x_location = models.IntegerField()
    y_location = models.IntegerField()
    inventory = models.ForeignKey(WhInventory, on_delete=models.CASCADE)



    


class userprofile(User):
    myaddress_x = models.IntegerField()
    myaddress_y = models.IntegerField()
    
class Order(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    create_time = models.DateTimeField()
    dst_x = models.IntegerField()
    dst_y = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_processed = models.BooleanField()

    status = models.TextField(blank = True)
    
class Truck(models.Model):
    truck_id = models.IntegerField()
    
