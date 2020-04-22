from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegisterForm,BuyProductForm
from .models import Product,Order,Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

def home(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'AmazonWeb/home.html', context)

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created successfully, you can log in now!')
            return redirect('login')
    else:
        form=UserRegisterForm()
    return render(request, 'AmazonWeb/register.html',{'form':form})


@login_required
def profile(request):
	return render(request,'AmazonWeb/profile.html')

@login_required
def history(request):
	user = User.objects.get(username=request.user.username)
	context={
		'orders': Order.objects.filter(user=user)
	}
	return render(request,'AmazonWeb/history.html',context)

@login_required
def buy(request):
	if request.method=='POST':
		form = BuyProductForm(request.POST)
		if form.is_valid():
			buyform=form.save()
			buyform.description=form.cleaned_data.get('description')
			product_name=form.cleaned_data.get('name')
			buyform.products=Product.objects.get(name=product_name)
			buyform.user=request.user
			buyform.save()
			messages.success(request,f'Account created successfully, you can log in now!')
			return redirect('AmazonWeb-home')
	else:
		form=UserRegisterForm()
		return render(request,'AmazonWeb/buy.html',{'form':BuyProductForm})

@login_required
def checkstatus(request):
	return render(request,'AmazonWeb/checkstatus.html')

@login_required
def search(request):
	query=request.GET.get('q')
	results=Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
	pages=pagination(request, results, num=1)
	context={
		'items':pages[0],
		'page_range':pages[1],
	}
	return render(request,'AmazonWeb/Search.html',context)