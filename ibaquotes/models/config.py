from django.db import models

class ConfigData(models.Model):

    company_name = models.CharField(max_length=150,)
    executive = models.CharField(max_length=150,)
    phone = models.CharField(max_length=150,)
    email = models.EmailField()
    address = models.CharField(max_length=150,)
    domain = models.CharField(max_length=100,null=True)
    offer_alias = models.CharField(max_length=150,)
    offer_number = models.IntegerField()