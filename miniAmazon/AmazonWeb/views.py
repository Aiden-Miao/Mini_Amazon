from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegisterForm

products=[
		{
		'name':'apple',
		'description':'a fruit Esther don\'t like',
		'price':'1 dollar',
		'id':'001'
		},
		{
		'name':'mango',
		'description':'a fruit Esther do like',
		'price':'2 dollar',
		'id':'002'
		}
]

def home(request):
    context = {
        'products': products
    }
    return render(request, 'AmazonWeb/home.html', context)

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            #messages.success(request,f'Account created successfully, you can log in now!')
            return redirect('login')
    else:
        form=UserRegisterForm()
    return render(request, 'AmazonWeb/register.html',{'form':form})

def history(request):
	return render(request,'AmazonWeb/history.html')

def buy(request):
	return render(request,'AmazonWeb/buy.html')

def checkstatus(request):
	return render(request,'AmazonWeb/checkstatus.html')