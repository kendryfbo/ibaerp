from django.contrib import admin
from django.urls import path,include
from ibaquotes import views

urlpatterns = [

    path('', views.index, name='index'),
    path('templatetest/', views.templatetest),
    # Product PATH
    path('product/list', views.product_list, name='product-list'),
    path('product/create/', views.product_create, name='product-create'),
    path('product/store/', views.product_store, name='product-store'),
    path('product/show/<int:id>', views.product_show, name='product-show'),
    path('product/edit/<int:id>', views.product_edit, name='product-edit'),
    path('product/update/<int:id>', views.product_update, name='product-update'),
    path('product/delete/<int:id>', views.product_delete, name='product-delete'),
    path('product/import/', views.product_import, name='product-import-file'),
    # client PATH
    path('client/list', views.client_list, name='client-list'),
    path('client/create/', views.client_create, name='client-create'),
    path('client/store/', views.client_store, name='client-store'),
    path('client/edit/<int:id>', views.client_edit, name='client-edit'),
    path('client/update/<int:id>', views.client_update, name='client-update'),
    path('client/show/<int:id>', views.client_show, name='client-show'),
    path('client/delete/<int:id>', views.client_delete, name='client-delete'),
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
