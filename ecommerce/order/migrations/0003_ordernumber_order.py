# Generated by Django 4.0.2 on 2022-03-18 04:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0002_alter_address_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordernumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_no', models.CharField(default=0, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15)),
                ('city', models.CharField(max_length=50)),
                ('pincode', models.CharField(max_length=10)),
                ('payment_method', models.CharField(max_length=10)),
                ('status', models.CharField(blank=True, choices=[('order_placed', 'order placed'), ('item_shipped', 'item shipped'), ('order_deliverd', 'order deliverd'), ('order_cancelled', 'order cancelled')], default='order placed', max_length=50, null=True)),
                ('total', models.PositiveBigIntegerField(blank=True, default=0, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product_stock', models.PositiveBigIntegerField(blank=True, default=0, null=True)),
                ('order_number', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='order.ordernumber')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
