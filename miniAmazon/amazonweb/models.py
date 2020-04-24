from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
# Create youur models here.                                                                                                                                                       
class Warehouse(models.Model):
    x_location = models.IntegerField()
    y_location = models.IntegerField()

class Product(models.Model):
    name = models.CharField(max_length = 200, default = "name")
    description = models.TextField(blank = True)
    price = models.DecimalField(max_digits = 9, decimal_places = 2,null=True)
    def __str__(self):
        return f'{self.name} Product'

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    myaddress_x = models.IntegerField(null=True,default=0)
    myaddress_y = models.IntegerField(null=True,default=0)
    def __str__(self):
        return f'{self.user.username} Profile'
    def save(self):
        super().save()

class Order(models.Model):
    #the fields user generate                                                                                                                                                     
    create_time = models.DateTimeField(default=datetime.now)
    dst_x = models.IntegerField()
    dst_y = models.IntegerField()
    products = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    #the fields that server generate                                                                                                                                              
    warehouse = models.ForeignKey(Warehouse, on_delete = models.CASCADE,null=True)
    is_processed = models.BooleanField(default=False)
    status = models.TextField(default="in progress")
    truck_id = models.IntegerField(null=True)
    def __str__(self):
        return f'{self.id} Order'

class Truck(models.Model):
    truck_num = models.IntegerField()
    warehouse = models.ForeignKey(Warehouse,on_delete=models.CASCADE,null=True)
