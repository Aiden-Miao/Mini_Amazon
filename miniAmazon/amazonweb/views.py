from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegisterForm,BuyProductForm,AddProductForm
from .models import Product,Order,Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'amazonweb/home.html', context)

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
    return render(request, 'amazonweb/register.html',{'form':form})


@login_required
def profile(request):
	return render(request,'amazonweb/profile.html')

@login_required
def history(request):
	user = User.objects.get(username=request.user.username)
	context={
		'orders': Order.objects.filter(user=user).order_by('-create_time')
	}
	return render(request,'amazonweb/history.html',context)


@login_required
def history_processing(request):
	user = User.objects.get(username=request.user.username)
	context={
		'orders': Order.objects.filter(user=user).filter(~Q(status='delivered')).order_by('-create_time')
	}
	return render(request,'amazonweb/history_processing.html',context)

@login_required
def history_completed(request):
	user = User.objects.get(username=request.user.username)
	context={
		'orders': Order.objects.filter(user=user).filter(status='delivered').order_by('-create_time')
	}
	return render(request,'amazonweb/history_completed.html',context)

@login_required
def buy(request):
	if request.method=='POST':
		form = BuyProductForm(request.POST)
		if form.is_valid():
			buyform=form.save()
			name=form.cleaned_data.get('name')
			try: 
				buyform.products=Product.objects.get(name=name)
			except ObjectDoesNotExist:
				messages.success(request,f'The product does not exist')
				return redirect(add)
			buyform.user=request.user
			buyform.save()
			messages.success(request,f'Successfully buy the product')
			return redirect(home)
	else:
		form=UserRegisterForm()
		return render(request,'amazonweb/buy.html',{'form':BuyProductForm})

def add(request):
	if request.method=='POST':
		form=AddProductForm(request.POST)
		if form.is_valid():
			addform=form.save()
			messages.success(request,f'Successfully add the product')
			return redirect(home)
	else:
		form=AddProductForm()
		return render(request,'amazonweb/add.html',{'form':AddProductForm})

@login_required
def checkstatus(request):
	return render(request,'amazonweb/checkstatus.html')

@login_required
def search(request):
	query=request.GET.get('q')
	results=Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
	pages=pagination(request, results, num=1)
	context={
		'items':pages[0],
		'page_range':pages[1],
	}
	return render(request,'amazonweb/Search.html',context)

def getOrder(query=None):
	order=Order.objects.get(id=query)
	return order 

def trackOrder(request):
	context={}
	query=""
	if request.GET:
		query=request.GET['q']
		context['query']=str(query)
		order=getOrder(query)
		context['order']=order
	return render(request,"amazonweb/track_order.html",context)
