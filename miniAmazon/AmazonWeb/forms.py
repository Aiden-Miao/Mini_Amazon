from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Order, Product

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class BuyProductForm(forms.ModelForm):
	name=forms.CharField(required=True,label="Product")
	#description=forms.CharField(required=False)
	class Meta:
		model=Order
		fields=['quantity','dst_x','dst_y']

class AddProductForm(forms.ModelForm):
	class Meta:
		model=Product
		fields=['name','description','price']
