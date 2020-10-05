from django.db import models

class QuotesAgreement(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):

        return self.name