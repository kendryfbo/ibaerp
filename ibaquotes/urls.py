from django.contrib import admin
from django.urls import path,include
from ibaquotes import views

urlpatterns = [
    path('', views.index),
]