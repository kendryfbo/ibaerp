# Generated by Django 3.1.2 on 2020-11-15 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibaquotes', '0018_auto_20201115_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='configdata',
            name='domain',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
