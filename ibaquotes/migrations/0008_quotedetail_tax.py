# Generated by Django 3.1.2 on 2020-11-09 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibaquotes', '0007_configdata_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotedetail',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
    ]