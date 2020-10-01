from django.db import models


class ProductStatus(models.Model):

    name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    
    def __str__(self):

        return self.name

class Product(models.Model):

    id = models.AutoField(primary_key=True)
    pdid = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    desc1 = models.CharField(max_length=100)
    desc2 = models.CharField(max_length=100)
    detail = models.TextField()
    remarks = models.TextField()
    status = models.ForeignKey(ProductStatus,on_delete=models.SET_NULL,null=True)
    price= models.DecimalField(decimal_places=2,max_digits=10)
    date = models.DateTimeField()
    Handlager = models.IntegerField()
    lang_id = models.IntegerField()
    weight = models.DecimalField(decimal_places=2,max_digits=10)
    ptype = models.CharField(max_length=10)
    HarmonizedCode = models.IntegerField()
    eccn = models.CharField(max_length=10)
    lkz = models.chareccn = models.CharField(max_length=2)
    ag = models.chareccn = models.CharField(max_length=1)
    imageurl = models.chareccn = models.CharField(max_length=100)
    imagepath = models.chareccn = models.CharField(max_length=100)

    def __str__(self):

        return self.name