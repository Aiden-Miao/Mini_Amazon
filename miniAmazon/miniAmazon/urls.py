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
from amazonweb import views as amazonweb_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('amazonweb.urls')),
    path('register/', amazonweb_views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='amazonweb/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='amazonweb/logout.html'),name='logout'),
    path('profile/',amazonweb_views.profile,name='profile'),
    path('history/',amazonweb_views.history,name='history'),
    path('history_processing/',amazonweb_views.history_processing,name='history_processing'),
    path('history_completed/',amazonweb_views.history_completed,name='history_completed'),
    path('buy/',amazonweb_views.buy,name='buy'),
    path('checkstatus/',amazonweb_views.checkstatus,name='checkstatus'),
    path('trackorder/',amazonweb_views.trackOrder,name='trackorder'),
    path('search/',amazonweb_views.search,name='search'),
    path('add/',amazonweb_views.add,name='add'),
]
