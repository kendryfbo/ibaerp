from django.contrib import admin
from django.urls import path,include
from ibaquotes import views

urlpatterns = [

    path('', views.index, name='index'),
    path('templatetest/', views.templatetest),

    path('product/list', views.product_list, name='product-list'),
    path('product/create/', views.create_product, name='product-create'),
    path('product/store/', views.store_product, name='product-store'),
    path('product/import/', views.import_product, name='product-import-file'),
    
    # Agreements PATH
    path('agreement/list', views.agreement_list, name='agreement-list'),
    path('agreement/create', views.agreement_create, name='agreement-create'),
    path('agreement/store', views.agreement_store, name='agreement-store'),
    
    # Quotes PATH
    path('list/', views.quote_list, name='quote-list'),
    path('create/', views.quote_create, name='quote-create'),
    path('store/', views.quote_store, name='quote-store'),
    path('edit/<int:id>', views.quote_edit, name='quote-edit'),
    path('update/<int:id>', views.quote_update, name='quote-update'),
    path('copy/<int:id>', views.quote_copy, name='quote-copy'),
    path('show/<int:id>', views.quote_show, name='quote-show'),
    path('delete/<int:id>', views.quote_delete, name='quote-delete'),
    path('pdf/<int:id>', views.quote_pdf, name='quote-pdf'),

    # PDF
   


]
