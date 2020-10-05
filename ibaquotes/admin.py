from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import ProductResource
from ibaquotes.models import Product, ProductStatus


admin.site.site_header = 'IBAERP Admin Dashboard'


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name','price','status',)
    ordering = ('name','price', 'status',)
    resource_class = ProductResource
    search_fields = ['name']



admin.site.register(Product,ProductAdmin)
admin.site.register(ProductStatus)