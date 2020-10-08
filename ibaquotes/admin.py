from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import ProductResource
from ibaquotes.models import Product, ProductStatus, ShippingTerm, PaymentCondition, QuotesAgreement 


admin.site.site_header = 'IBAERP Admin Dashboard'


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('pdid','name','price','status',)
    ordering = ('pdid','name','price', 'status',)
    resource_class = ProductResource
    search_fields = ['pdid','name']



admin.site.register(Product,ProductAdmin)
admin.site.register(ProductStatus)
admin.site.register(ShippingTerm)
admin.site.register(PaymentCondition)
admin.site.register(QuotesAgreement)