# Generated by Django 3.1.2 on 2021-04-15 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibaquotes', '0033_auto_20201213_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='payment_condition_days',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='quote',
            name='payment_condition_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='quote',
            name='shipping_term_name',
            field=models.CharField(max_length=100),
        ),
    ]
