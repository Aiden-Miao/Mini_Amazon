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

"""
class Inventory(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
"""

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    myaddress_x = models.IntegerField(null=True,default=0)
    myaddress_y = models.IntegerField(null=True,default=0)
    def __str__(self):
        return f'{self.user.username} Profile'
    
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
    is_processed = models.BooleanField(default=False)
    status = models.TextField(default="packing")
    
class Truck(model.Model):
    truck_id = model.IntegerField()
    warehouse_id = models.ForeignKey(Warehouse)

    
