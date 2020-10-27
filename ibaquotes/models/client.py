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
    username = models.CharField(max_length=150,)
    cfname = models.CharField(max_length=150,)
    clname = models.CharField(max_length=150,)
    usergroup = models.IntegerField()
    cemail = models.CharField(max_length=150,)
    company = models.CharField(max_length=150,)
    newsletter = models.CharField(max_length=150,blank=True)
    address = models.CharField(max_length=150,blank=True)
    zipcode = models.CharField(max_length=150,blank=True)
    city = models.CharField(max_length=150,)
    country = models.CharField(max_length=150,)
    domain = models.CharField(max_length=150,)
    phone = models.CharField(max_length=150,)
    status = models.ForeignKey(ClientStatus,on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company +" - "+ self.cfname
    