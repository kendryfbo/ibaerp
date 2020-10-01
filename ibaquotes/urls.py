from django.contrib import admin
from django.urls import path,include
from ibaquotes import views

urlpatterns = [
    path('', views.index),
    path('templatetest/', views.templatetest),
    path('product/import/', views.import_product, name='product-import-file'),
]
