from django.db import models
from .client import Client
from .product import Product

class Currency(models.Model):

    class Meta: 
        verbose_name = 'Currency'
        verbose_name_plural = "Currencies"

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=5)
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.name




class ShippingTerm(models.Model):

    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class PaymentCondition(models.Model):

    name = models.CharField(max_length=100)
    days = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class QuotesAgreement(models.Model):

    name = models.CharField(max_length=100)
    shipping_terms = models.ForeignKey(ShippingTerm,on_delete=models.SET_NULL,null=True)
    payment_condition = models.ForeignKey(PaymentCondition,on_delete=models.SET_NULL,null=True)
    exp_days = models.IntegerField()
    description = models.TextField(max_length=1000)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

class Quote(models.Model):

    number = models.IntegerField()
    offer = models.CharField(max_length=50)
    request = models.CharField(max_length=50)
    client = models.ForeignKey(Client,on_delete=models.RESTRICT)
    client_name = models.CharField(max_length=150,)
    address = models.CharField(max_length=150,)
    executive = models.CharField(max_length=150,)
    phone = models.CharField(max_length=150,)
    email = models.EmailField()
    payment_condition = models.ForeignKey(PaymentCondition,on_delete=models.RESTRICT)
    shipping_term = models.ForeignKey(ShippingTerm,on_delete=models.RESTRICT)
    currency = models.ForeignKey(Currency,on_delete=models.RESTRICT)
    description = models.TextField()
    date = models.DateTimeField()
    weight = models.DecimalField(max_digits=19,decimal_places=2)
    subtotal = models.DecimalField(max_digits=19,decimal_places=2)
    taxes = models.DecimalField(max_digits=19,decimal_places=2)
    total = models.DecimalField(max_digits=19,decimal_places=2)
    weight = models.DecimalField(max_digits=19,decimal_places=2)
    exp_date = models.DateTimeField()
    copy = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.request)

class QuoteDetail(models.Model):
    
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE)
    group_num = models.IntegerField()
    group_name = models.CharField(max_length=50)
    item_num = models.IntegerField()
    product = models.ForeignKey(Product,on_delete=models.RESTRICT)
    product_name = models.CharField(max_length=150)
    product_detail = models.TextField(max_length=150,null=True)
    product_remarks = models.TextField(max_length=150,null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=19,decimal_places=2)
