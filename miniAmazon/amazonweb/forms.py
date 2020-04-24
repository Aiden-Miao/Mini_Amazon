from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Order, Product,Profile

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class BuyProductForm(forms.ModelForm):
	name=forms.CharField(required=True,label="Product")
	class Meta:
		model=Order
		fields=['quantity','dst_x','dst_y']

class AddProductForm(forms.ModelForm):
	class Meta:
		model=Product
		fields=['name','description','price']


class UpdateEmailForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email']


class  UpdateProfileForm(forms.ModelForm):
	class Meta:
		model=Profile 
		fields=['myaddress_x','myaddress_y']
		labels=['X coordinate','Y coordinate']