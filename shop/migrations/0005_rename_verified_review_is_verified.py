# Generated by Django 5.2 on 2025-04-23 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_purchase_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='verified',
            new_name='is_verified',
        ),
    ]
