from django.db import models


class ProductStatus(models.Model):
    name = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    class Meta: 
        db_table = 'product_status'
        verbose_name = 'Product Status'
        verbose_name_plural = 'Product Status'

class Product(models.Model):

    class Meta: 
        verbose_name = 'Product'

    pdid = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=100)
    descr1 = models.TextField(max_length=100)
    descr2 = models.TextField(max_length=100)
    detail = models.TextField(max_length=150,null=True)
    remarks = models.TextField(max_length=150,null=True)
    status = models.ForeignKey(ProductStatus,on_delete=models.SET_NULL,null=True)
    price= models.DecimalField(decimal_places=2,max_digits=10)
    date = models.DateField()
    handlager = models.IntegerField() # fix capital name
    lang_id = models.IntegerField()
    weight = models.DecimalField(decimal_places=2,max_digits=10)
    ptype = models.CharField(max_length=15)
    harmonizedcode = models.IntegerField() # fix capital name
    eccn = models.CharField(max_length=10)
    lkz =  models.CharField(max_length=2)
    ag = models.CharField(max_length=1)
    imageurl = models.CharField(max_length=100,blank=True,default='')
    imagepath = models.CharField(max_length=100,blank=True,default='')

    def __str__(self):
        return self.name
    