# Generated by Django 2.2.8 on 2021-06-21 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_backend', '0004_auto_20210616_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='state_or_province',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]