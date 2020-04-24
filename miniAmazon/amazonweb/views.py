from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegisterForm,BuyProductForm,AddProductForm,UpdateProfileForm,UpdateEmailForm
from .models import Product,Order,Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

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
	if request.method=='POST':
		email=UpdateEmailForm(request.POST,instance=request.user)
		the_profile=Profile.objects.get(user=request.user)
		profile=UpdateProfileForm(request.POST,instance=the_profile)
		if profile.is_valid() and email.is_valid():
			profile.save()
			email.save()
			messages.success(request,f'User Profile have been updated successfully.')
			send_mail(
			    'Update Profile-Mini Amazon',
			    'You have updated your profile successfully',
			    'Mini Amazon',
			    [request.user.email],
			    fail_silently=False,
			)
			return redirect(home)
	else:
		profile=UpdateProfileForm(instance=request.user)
		the_profile=Profile.objects.get(user=request.user)
		email=UpdateEmailForm(instance=the_profile)
		context={
			'profile_form':profile,
			'email_form':email,
			'the_profile':the_profile
		}
		return render(request,'amazonweb/profile.html',context)

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
		the_profile=Profile.objects.get(user=request.user)
		form = BuyProductForm(request.POST,initial={'dst_x':the_profile.myaddress_x,'dst_y':the_profile.myaddress_y})
		if form.is_valid():
			#CHECK IF THE ITEM EXISTS
			name=form.cleaned_data.get('name')
			try:
				the_product=Product.objects.get(name=name)
				buyform=form.save()
				buyform.products=the_product
				buyform.user=request.user
				buyform.save()
				messages.success(request,f'Successfully buy the product')
				send_mail(
				    'Order Being Processed-Mini Amazon',
				    'Thank you for shopping with us, your order is in process.',
				    'Mini Amazon',
				    [request.user.email],
				    fail_silently=False,
				)
				return redirect(home)
			except ObjectDoesNotExist:
				messages.success(request,f'The product does not exist')
				return redirect(add)
	else:
		the_profile=Profile.objects.get(user=request.user)
		form=BuyProductForm(initial={'dst_x':the_profile.myaddress_x,'dst_y':the_profile.myaddress_y})
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
	try:
		order=Order.objects.get(id=query)
		return order
	except ObjectDoesNotExist:
		return None

def trackOrder(request):
	context={}
	query=""
	if request.GET:
		query=request.GET['q']
		context['query']=str(query)
		order=getOrder(query)
		context['order']=order
		context['is_search']=True
		return render(request,"amazonweb/track_order.html",context)
	else:
		context['is_search']=False
		return render(request,"amazonweb/track_order.html",context)