# Generated by Django 3.1.2 on 2020-11-17 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibaquotes', '0020_auto_20201117_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ag',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='descr2',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='eccn',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='handlager',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='harmonizedcode',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='imagepath',
            field=models.ImageField(null=True, upload_to='products'),
        ),
        migrations.AlterField(
            model_name='product',
            name='imageurl',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='lang_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='lkz',
            field=models.CharField(max_length=2, null=True),
        ),
    ]
