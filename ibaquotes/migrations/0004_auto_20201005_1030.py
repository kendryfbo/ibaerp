# Generated by Django 3.1 on 2020-10-05 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibaquotes', '0003_auto_20201004_2049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Handlager',
            new_name='handlager',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='HarmonizedCode',
            new_name='harmonizedcode',
        ),
        migrations.RenameField(
            model_name='productstatus',
            old_name='status',
            new_name='active',
        ),
    ]
