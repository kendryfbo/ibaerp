from django.db import models

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
    description = models.TextField(max_length=250)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name