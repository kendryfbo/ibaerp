from django.contrib import admin
from django.urls import path,include
from ibaquotes import views

urlpatterns = [

    path('', views.index),
    path('templatetest/', views.templatetest),

    path('product/create/', views.create_product, name='product-create'),
    path('product/store/', views.store_product, name='product-store'),
    path('product/import/', views.import_product, name='product-import-file'),

    path('agreement/create', views.create_agreement, name='agreement-create'),
    path('agreement/store', views.store_agreement, name='agreement-store')
]
