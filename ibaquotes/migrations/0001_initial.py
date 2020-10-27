# Generated by Django 3.1.2 on 2020-10-18 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Client Status',
                'verbose_name_plural': 'Client Status',
                'db_table': 'client_status',
            },
        ),
        migrations.CreateModel(
            name='PaymentCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('days', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Product Status',
                'verbose_name_plural': 'Product Status',
                'db_table': 'product_status',
            },
        ),
        migrations.CreateModel(
            name='ShippingTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuotesAgreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('exp_days', models.IntegerField()),
                ('description', models.TextField(max_length=250)),
                ('active', models.BooleanField(default=True)),
                ('payment_condition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ibaquotes.paymentcondition')),
                ('shipping_terms', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ibaquotes.shippingterm')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdid', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('descr1', models.TextField(max_length=100)),
                ('descr2', models.TextField(max_length=100)),
                ('detail', models.TextField(max_length=150, null=True)),
                ('remarks', models.TextField(max_length=150, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('handlager', models.IntegerField()),
                ('lang_id', models.IntegerField()),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ptype', models.CharField(max_length=15)),
                ('harmonizedcode', models.IntegerField()),
                ('eccn', models.CharField(max_length=10)),
                ('lkz', models.CharField(max_length=2)),
                ('ag', models.CharField(max_length=1)),
                ('imageurl', models.CharField(blank=True, default='', max_length=100)),
                ('imagepath', models.CharField(blank=True, default='', max_length=100)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ibaquotes.productstatus')),
            ],
            options={
                'verbose_name': 'Product',
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('cfname', models.CharField(max_length=150)),
                ('clname', models.CharField(max_length=150)),
                ('usergroup', models.IntegerField()),
                ('cemail', models.CharField(max_length=150)),
                ('company', models.CharField(max_length=150)),
                ('newsletter', models.CharField(max_length=150)),
                ('address', models.CharField(blank=True, max_length=150)),
                ('zipcode', models.CharField(blank=True, max_length=150)),
                ('city', models.CharField(max_length=150)),
                ('country', models.CharField(max_length=150)),
                ('domain', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ibaquotes.clientstatus')),
            ],
        ),
    ]
