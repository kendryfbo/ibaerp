from django.contrib import admin
from django.urls import path,include
from ibaquotes import views

urlpatterns = [

    path('', views.index),
    path('templatetest/', views.templatetest),

    path('product/list', views.product_list, name='product-list'),
    path('product/create/', views.create_product, name='product-create'),
    path('product/store/', views.store_product, name='product-store'),
    path('product/import/', views.import_product, name='product-import-file'),

    path('agreement/list', views.agreement_list, name='agreement-list'),
    path('agreement/create', views.agreement_create, name='agreement-create'),
    path('agreement/store', views.agreement_store, name='agreement-store')
]
