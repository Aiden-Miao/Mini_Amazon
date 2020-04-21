from django.db import models
from django.contrib.auth import User
from django.utils import timezone

# Create youur models here.
class Warehouse(models.Model):
    #do we need wh_id?
    wh_id = models.IntegerField()
    x_location = models.IntegerField()
    y_location = models.IntegerField()
    
class Product(models.Model):
    product_id = models.IntegerField()
    name = models.CharField(max_length = 200, default = "name")
    description = models.TextField(blank = True)
    price = models.DecimalField(max_digits = 9, decimal_places = 2)

"""
class Items(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    num = models.IntegerField()
"""
"""
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    all_items = models.ForeignKey(Items, on_delete=models.CASCADE)
"""

class userprofile(User):
    myaddress_x = models.IntegerField()
    myaddress_y = models.IntegerField()
    
class Order(models.Model):
    create_time = models.DataTimeField()
    #update_time = models.DataTimeField()
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    #total_price = models.DecimalField(max_digits = 9, decimal_places = 2)
    order_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dst_x = models.IntegerField()
    dst_y = models.IntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    status = models.TextField(blank = True)
    
class Truck(model.Model):
    truck_id = model.IntegerField()
    #why?
    warehouse_id = models.ForeignKey(Warehouse)
    
#what is purchase more?
