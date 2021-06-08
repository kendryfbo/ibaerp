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
    pdf_top_msg = models.TextField(max_length=1500,null=True)
    pdf_img_msg = models.TextField(max_length=150,null=True)
    pdf_observ_msg = models.TextField(max_length=1500,null=True)
    company_img = models.ImageField(upload_to='company',null=True,blank=True)

    def __str__(self):
        return self.company_name

    class Meta: 
        verbose_name = 'Config Data'
        verbose_name_plural = 'Config Data' 
