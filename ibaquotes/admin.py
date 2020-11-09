from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .resources import ProductResource
from ibaquotes.models import Product, ProductStatus, ShippingTerm, PaymentCondition 
from ibaquotes.models import QuotesAgreement, Client, ClientStatus, Currency
from ibaquotes.models import Quote, QuoteDetail, ConfigData


admin.site.site_header = 'IBAERP Admin Dashboard'


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('pdid','name','price','status','image_tag',)
    ordering = ('pdid','name','price', 'status',)
    resource_class = ProductResource
    search_fields = ['pdid','name']
    readonly_fields = ('image_tag',)
    #fields = ('image_tag','pdid','name','price',)

    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.imageurl))

    image_tag.short_description = 'Picture'


admin.site.register(Product,ProductAdmin)
admin.site.register(ProductStatus)
admin.site.register(ShippingTerm)
admin.site.register(PaymentCondition)
admin.site.register(QuotesAgreement)
admin.site.register(ClientStatus)
admin.site.register(Client)
admin.site.register(Currency)
admin.site.register(Quote)
admin.site.register(QuoteDetail)
admin.site.register(ConfigData)