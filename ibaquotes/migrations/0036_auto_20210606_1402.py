# Generated by Django 3.1.2 on 2021-06-06 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibaquotes', '0035_auto_20210606_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='descr1',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='descr2',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='detail',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='remarks',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='quotedetail',
            name='product_detail',
            field=models.TextField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='quotedetail',
            name='product_remarks',
            field=models.TextField(max_length=200, null=True),
        ),
    ]