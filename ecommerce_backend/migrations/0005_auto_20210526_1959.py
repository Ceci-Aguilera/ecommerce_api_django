# Generated by Django 2.2.8 on 2021-05-26 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_backend', '0004_auto_20210526_1956'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_active',
            new_name='active',
        ),
    ]
