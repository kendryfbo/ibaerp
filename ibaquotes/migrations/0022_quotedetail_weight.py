# Generated by Django 3.1.2 on 2020-11-24 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibaquotes', '0021_auto_20201117_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotedetail',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
            preserve_default=False,
        ),
    ]
