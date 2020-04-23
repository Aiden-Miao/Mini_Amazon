"""miniAmazon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from AmazonWeb import views as AmazonWeb_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('AmazonWeb.urls')),
    path('register/', AmazonWeb_views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='AmazonWeb/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='AmazonWeb/logout.html'),name='logout'),
    path('profile/',AmazonWeb_views.profile,name='profile'),
    path('history/',AmazonWeb_views.history,name='history'),
    path('history_processing/',AmazonWeb_views.history_processing,name='history_processing'),
    path('history_completed/',AmazonWeb_views.history_completed,name='history_completed'),
    path('buy/',AmazonWeb_views.buy,name='buy'),
    path('checkstatus/',AmazonWeb_views.checkstatus,name='checkstatus'),
    path('trackorder/',AmazonWeb_views.trackOrder,name='trackorder'),
    path('search/',AmazonWeb_views.search,name='search'),
    path('add/',AmazonWeb_views.add,name='add'),
]
