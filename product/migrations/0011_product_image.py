# Generated by Django 4.2.3 on 2023-07-19 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_delete_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
    ]