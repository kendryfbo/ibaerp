# Generated by Django 3.1.2 on 2020-11-09 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibaquotes', '0013_auto_20201109_1041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='imageurl',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products'),
        ),
    ]
