# Generated by Django 3.1.2 on 2020-11-14 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibaquotes', '0015_auto_20201109_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='quote',
            name='exp_date',
            field=models.DateField(),
        ),
    ]