from django.db import models

class ClientStatus(models.Model):
    name = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    class Meta: 
        db_table = 'client_status'
        verbose_name = 'Client Status'
        verbose_name_plural = 'Client Status'

class Client(models.Model):
    username = models.CharField()
    cfname = models.CharField()
    clname = models.CharField()
    usergroup = models.IntegerField()
    cemail = models.CharField()
    company = models.CharField()
    newsletter = models.CharField()
    address = models.CharField(blank=True)
    zipcode = models.CharField(blank=True)
    city = models.CharField()
    country = models.CharField()
    domain = models.CharField()
    phone = models.CharField()
    status = models.ForeignKey(ProductStatus,on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    