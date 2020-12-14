# Generated by Django 3.1.2 on 2020-12-13 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibaquotes', '0031_remove_client_usergroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='business_area',
            field=models.CharField(default='Not provided', max_length=150),
        ),
        migrations.AddField(
            model_name='quote',
            name='project_name',
            field=models.CharField(default='Not provided', max_length=50),
        ),
    ]