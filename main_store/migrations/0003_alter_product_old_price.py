# Generated by Django 4.2.16 on 2024-11-23 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_store', '0002_alter_product_old_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
    ]
