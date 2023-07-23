# Generated by Django 4.2.3 on 2023-07-18 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_remove_cart_product_alter_cart_user'),
        ('product', '0004_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.cart'),
        ),
    ]