# Generated by Django 2.2.8 on 2021-06-26 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_backend', '0005_address_state_or_province'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=256),
        ),
    ]
