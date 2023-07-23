# Generated by Django 4.2.3 on 2023-07-19 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_remove_product_cart'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
