from django.contrib import admin
from . import views
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='amazon-home'),
]

